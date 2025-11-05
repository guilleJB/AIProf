"""
Streamlit demo per fer una prova conceptual de l'alumne amb AIProf.
Permet:
1. Seleccionar nivell i tema per obtenir un exercici del backend (MCP).
2. Escriure una resposta i enviar-la com a xAPI statement.
3. Registrar la interacció en un log local de validació.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import streamlit as st

BACKEND_URL = os.getenv("AIPROF_BACKEND_URL", "http://localhost:8000")
VALIDATION_LOG = Path(__file__).resolve().parents[1] / "data" / "validation_log.jsonl"


def log_validation(entry: dict[str, Any]) -> None:
    VALIDATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def fetch_curriculum(level: str, base_url: str, subject: str | None = None) -> list[dict[str, Any]]:
    params = {"subject": subject} if subject else None
    response = requests.get(f"{base_url}/mcp/curriculum/{level}", params=params, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Currículum no disponible ({response.status_code})")
    return response.json().get("modules", [])


def send_statement(payload: dict[str, Any], base_url: str) -> None:
    response = requests.post(f"{base_url}/xapi/statements", json=payload, timeout=10)
    response.raise_for_status()


def build_statement(student: str, exercise: dict[str, Any], answer: str) -> dict[str, Any]:
    now = datetime.utcnow().isoformat() + "Z"
    context_parent = {"id": f"http://aiprof.local/curriculum/{exercise['id']}"}
    context = {"contextActivities": {"parent": [context_parent]}}
    if exercise.get("subject"):
        context["contextActivities"]["category"] = [
            {"id": f"http://aiprof.local/subject/{exercise['subject']}"}
        ]
    return {
        "actor": {"name": student, "mbox": f"mailto:{student.replace(' ', '').lower()}@aiprof.local"},
        "verb": {"id": "http://adlnet.gov/expapi/verbs/answered", "display": {"en": "answered"}},
        "object": {
            "id": f"http://aiprof.local/exercise/{exercise['id']}",
            "definition": {
                "name": {"ca": exercise["title"]},
                "description": {"ca": exercise.get("example_exercise", "")},
            },
        },
        "result": {"response": answer},
        "context": context,
        "timestamp": now,
    }


def main() -> None:
    st.set_page_config(page_title="AIProf Demo", page_icon="🧪", layout="centered")
    st.title("🧩 AIProf · Prova conceptual")
    st.caption("Simula una interacció bàsica d’alumne amb el backend MCP + xAPI.")

    st.sidebar.subheader("Configuració")
    backend_url = st.sidebar.text_input("Backend URL", value=BACKEND_URL)
    st.sidebar.write("Executa `uvicorn backend.main:app --reload` abans de començar.")

    student_name = st.text_input("Nom de l'alumne", value="Alex Pupil")
    level = st.selectbox("Nivell", options=["1eso", "3eso"])

    available_subjects: list[str] | None = None
    if "subject_cache" not in st.session_state:
        st.session_state.subject_cache = {}

    cache = st.session_state.subject_cache
    if level not in cache:
        try:
            fetched = fetch_curriculum(level, backend_url)
            subjects = sorted({module.get("subject", "") for module in fetched if module.get("subject")})
            cache[level] = subjects
        except Exception:
            cache[level] = []

    available_subjects = cache.get(level, [])
    subject = st.selectbox(
        "Assignatura",
        options=["(Totes)"] + available_subjects if available_subjects else ["(Totes)"]
    )
    subject_filter = None if subject == "(Totes)" else subject

    if "exercise" not in st.session_state:
        st.session_state.exercise = None
    if "modules" not in st.session_state:
        st.session_state.modules = []

    if st.button("Obtenir exercici"):
        try:
            modules = fetch_curriculum(level, backend_url, subject_filter)
            if not modules:
                st.warning("No hi ha contingut per aquest nivell/assignatura.")
            else:
                st.session_state.modules = modules
                st.session_state.exercise = modules[0]
                st.success(f"Exercici carregat: {modules[0]['title']}")
        except Exception as exc:  # pragma: no cover - UX feedback
            st.error(f"Error obtenint currículum: {exc}")

    if st.session_state.modules:
        options = {module["title"]: module for module in st.session_state.modules}
        selected_title = st.selectbox(
            "Selecciona el mòdul",
            options=list(options.keys()),
            key="module_selector",
        )
        st.session_state.exercise = options[selected_title]

    exercise = st.session_state.exercise
    if exercise:
        st.subheader("Enunciat")
        st.write(f"**{exercise['title']}**")
        st.info(exercise.get("example_exercise", "Sense enunciat."))

        answer = st.text_area("Resposta de l'alumne", height=150)
        if st.button("Enviar resposta"):
            statement = build_statement(student_name, exercise, answer)
            try:
                send_statement(statement, backend_url)
                log_validation(
                    {
                        "student": student_name,
                        "level": level,
                        "subject": exercise.get("subject"),
                        "exercise": exercise["id"],
                        "answer": answer,
                        "timestamp": statement["timestamp"],
                    }
                )
                st.success("Resposta enviada i registrada!")
            except Exception as exc:  # pragma: no cover
                st.error(f"No s'ha pogut enviar la resposta: {exc}")

    st.divider()
    st.caption(f"Les interaccions es registren a `{VALIDATION_LOG}`.")


if __name__ == "__main__":
    main()
