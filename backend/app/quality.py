from typing import Any
SUPPORTED_TYPES={"Patient","Observation","Encounter"}
def validate_resource(resource:dict[str,Any])->dict[str,Any]:
    issues=[]; kind=resource.get("resourceType")
    if kind not in SUPPORTED_TYPES:
        issues.append({"severity":"error","code":"unsupported-resource","message":"resourceType must be Patient, Observation, or Encounter"})
        return {"valid":False,"score":0,"issues":issues,"dimensions":{"completeness":0,"validity":0,"consistency":0,"uniqueness":100}}
    required={"Patient":["name","gender"],"Observation":["status","code","subject"],"Encounter":["status","class","subject"]}[kind]
    missing=[f for f in required if not resource.get(f)]
    for f in missing: issues.append({"severity":"warning","code":"missing-required-data","message":f"Missing recommended field: {f}"})
    if kind=="Patient" and resource.get("gender") not in {None,"male","female","other","unknown"}: issues.append({"severity":"error","code":"invalid-gender","message":"Invalid Patient.gender code"})
    if kind=="Observation" and resource.get("status") not in {"registered","preliminary","final","amended","corrected","cancelled","entered-in-error","unknown"}: issues.append({"severity":"error","code":"invalid-observation-status","message":"Invalid Observation.status code"})
    if kind=="Encounter" and resource.get("status") not in {"planned","in-progress","on-hold","discharged","completed","cancelled","discontinued","entered-in-error","unknown"}: issues.append({"severity":"error","code":"invalid-encounter-status","message":"Invalid Encounter.status code"})
    ref=resource.get("subject")
    if ref is not None and (not isinstance(ref,dict) or not isinstance(ref.get("reference"),str)): issues.append({"severity":"error","code":"invalid-reference","message":"subject must contain a reference string"})
    errors=sum(i["severity"]=="error" for i in issues); warnings=sum(i["severity"]=="warning" for i in issues)
    completeness=round(100*(len(required)-len(missing))/len(required)); validity=max(0,100-errors*25)
    consistency=100 if not any(i["code"]=="invalid-reference" for i in issues) else 50
    score=max(0,round(completeness*.3+validity*.5+consistency*.2)-warnings*2)
    return {"valid":errors==0,"score":score,"issues":issues,"dimensions":{"completeness":completeness,"validity":validity,"consistency":consistency,"uniqueness":100}}
