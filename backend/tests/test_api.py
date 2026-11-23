def test_health(client):
    r=client.get("/health"); assert r.status_code==200 and r.json()["fhir_version"]=="R4"
def test_validate_endpoint(client):
    r=client.post("/api/v1/validate",json={"resourceType":"Patient","name":[{"family":"Synthetic"}],"gender":"unknown"})
    assert r.status_code==200 and r.json()["valid"] is True
def test_ingest_and_metrics(client):
    p={"resourceType":"Patient","id":"synthetic-001","name":[{"family":"Sample"}],"gender":"unknown"}
    assert client.post("/api/v1/resources",json=p).status_code==201
    assert client.get("/api/v1/resources").json()[0]["id"]=="synthetic-001"
    assert client.get("/api/v1/metrics").json()["resources"]==1
def test_duplicate_resource_conflicts(client):
    p={"resourceType":"Patient","id":"synthetic-dup","name":[{"family":"Sample"}],"gender":"unknown"}
    client.post("/api/v1/resources",json=p); assert client.post("/api/v1/resources",json=p).status_code==409
