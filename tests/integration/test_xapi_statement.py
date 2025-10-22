import pytest


pytestmark = pytest.mark.integration


def test_xapi_statement_is_persisted(client, memory_store):
    payload = {
        "actor": {"mbox": "mailto:student@example.com"},
        "verb": {"id": "http://adlnet.gov/expapi/verbs/answered"},
        "object": {"id": "http://aiprof.example.com/exercises/math-1"},
        "result": {"score": {"raw": 0.8}},
    }

    response = client.post("/xapi/statements", json=payload)

    assert response.status_code == 202
    assert response.json()["status"] == "queued"
    assert len(memory_store.statements) == 1
    assert memory_store.statements[0]["verb"]["id"].endswith("answered")
