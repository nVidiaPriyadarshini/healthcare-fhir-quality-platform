from datetime import datetime,timezone
from sqlalchemy import DateTime,Integer,JSON,String
from sqlalchemy.orm import Mapped,mapped_column
from .db import Base
class ResourceRecord(Base):
    __tablename__="resources"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    resource_type:Mapped[str]=mapped_column(String(64),index=True)
    resource_id:Mapped[str]=mapped_column(String(128),unique=True,index=True)
    payload:Mapped[dict]=mapped_column(JSON)
    quality_score:Mapped[int]=mapped_column(Integer,default=100)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
class ValidationRun(Base):
    __tablename__="validation_runs"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    resource_id:Mapped[str]=mapped_column(String(128),index=True)
    status:Mapped[str]=mapped_column(String(24))
    issues:Mapped[list]=mapped_column(JSON,default=list)
    score:Mapped[int]=mapped_column(Integer)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
