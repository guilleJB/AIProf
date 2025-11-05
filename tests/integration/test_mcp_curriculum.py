import pytest


pytestmark = pytest.mark.integration


def test_fetch_curriculum_level(client):
    response = client.get("/mcp/curriculum/1eso")
    assert response.status_code == 200
    payload = response.json()
    assert payload["level"] == "1eso"
    assert len(payload["modules"]) >= 1
    assert payload["modules"][0]["title"]


def test_fetch_curriculum_filtered_by_subject(client):
    response = client.get("/mcp/curriculum/1eso", params={"subject": "castellà"})
    assert response.status_code == 200
    modules = response.json()["modules"]
    assert all(module["subject"] == "castellà" for module in modules)


def test_fetch_single_module(client):
    response = client.get("/mcp/curriculum/1eso/modules/lengua-generos-literarios")
    assert response.status_code == 200
    module = response.json()
    assert module["id"] == "lengua-generos-literarios"
    assert module["title"].lower().startswith("gèneres literaris")


def test_generate_exercise_from_module(client):
    response = client.post(
        "/mcp/exercises/generate",
        json={"level": "1eso", "module_id": "lengua-elementos-comunicacion"},
    )
    assert response.status_code == 200
    exercise = response.json()
    assert exercise["module_id"] == "lengua-elementos-comunicacion"
    assert "Respon" in exercise["instructions"]
    assert "Unitat" in exercise["prompt"]


def test_assess_exercise_feedback(client):
    exercise_response = client.post(
        "/mcp/exercises/generate",
        json={"level": "1eso", "module_id": "lengua-elementos-comunicacion"},
    )
    exercise = exercise_response.json()
    assessment_response = client.post(
        "/mcp/exercises/assess",
        json={
            "exercise": exercise,
            "answer": "L'emissor envia el missatge pel canal utilitzant un codi compartit.",
        },
    )
    assert assessment_response.status_code == 200
    feedback = assessment_response.json()
    assert feedback["score"] is not None
    assert "conceptes" in feedback["feedback"].lower()
