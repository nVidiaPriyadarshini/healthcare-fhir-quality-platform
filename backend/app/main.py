import os
from contextlib import asynccontextmanager
from fastapi import Depends,FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from .db import Base,engine,get_db
from .models import ResourceRecord,ValidationRun
from .quality import validate_resource
@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
app=FastAPI(title="Healthcare FHIR Quality Platform",version="1.0.0",lifespan=lifespan)
# Set CORS_ORIGINS to a comma-separated list of trusted frontend origins.
# A wildcard is suitable only for this unauthenticated, synthetic-data demo.
cors_origins=os.getenv("CORS_ORIGINS","http://localhost:5173,http://localhost:4173")
app.add_middleware(CORSMiddleware,allow_origins=[origin.strip() for origin in cors_origins.split(",") if origin.strip()],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
@app.get("/health")
def health(): return {"status":"ok","fhir_version":"R4"}
@app.post("/api/v1/validate")
def validate(payload:dict,db:Session=Depends(get_db)):
    result=validate_resource(payload); rid=payload.get("id") or "unidentified"
    db.add(ValidationRun(resource_id=rid,status="valid" if result["valid"] else "invalid",issues=result["issues"],score=result["score"])); db.commit()
    return result
@app.post("/api/v1/resources",status_code=201)
def ingest(payload:dict,db:Session=Depends(get_db)):
    result=validate_resource(payload)
    if not payload.get("id"): raise HTTPException(422,"FHIR resource id is required")
    if not result["valid"]: raise HTTPException(422,detail={"message":"FHIR quality validation failed",**result})
    if db.scalar(select(ResourceRecord).where(ResourceRecord.resource_id==payload["id"])): raise HTTPException(409,"Resource id already exists")
    row=ResourceRecord(resource_type=payload["resourceType"],resource_id=payload["id"],payload=payload,quality_score=result["score"])
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.resource_id,"resourceType":row.resource_type,"quality_score":row.quality_score}
@app.get("/api/v1/resources")
def list_resources(limit:int=100,db:Session=Depends(get_db)):
    rows=db.scalars(select(ResourceRecord).order_by(ResourceRecord.id.desc()).limit(min(max(limit,1),500))).all()
    return [{"id":r.resource_id,"resourceType":r.resource_type,"quality_score":r.quality_score,"created_at":r.created_at} for r in rows]
@app.get("/api/v1/metrics")
def metrics(db:Session=Depends(get_db)):
    total=db.scalar(select(func.count(ResourceRecord.id))) or 0; avg=db.scalar(select(func.avg(ResourceRecord.quality_score))) or 0
    runs=db.scalar(select(func.count(ValidationRun.id))) or 0
    invalid=db.scalar(select(func.count(ValidationRun.id)).where(ValidationRun.status=="invalid")) or 0
    return {"resources":total,"average_quality":round(float(avg),1),"validation_runs":runs,"invalid_runs":invalid}
