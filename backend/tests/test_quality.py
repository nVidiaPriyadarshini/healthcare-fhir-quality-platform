from app.quality import validate_resource
def test_valid_patient_scores_well():
    r=validate_resource({"resourceType":"Patient","id":"demo-1","name":[{"family":"Example"}],"gender":"unknown"})
    assert r["valid"] is True and r["score"]>=90
def test_invalid_gender_is_error():
    r=validate_resource({"resourceType":"Patient","gender":"not-a-gender"})
    assert r["valid"] is False and any(i["code"]=="invalid-gender" for i in r["issues"])
def test_unsupported_resource_is_rejected():
    assert validate_resource({"resourceType":"Medication"})["valid"] is False
