# AIProf Agent Notes

This document recull l’estat actual del projecte i les pautes per continuar treballant-hi des de Codex o qualsevol altre agent.

## Context del projecte
- **Nom:** AIProf
- **Objectiu:** Professor virtual per alumnat de 1r i 3r d’ESO amb generació d’exercicis, correcció, adaptació de nivell i registre xAPI en un LRS.
- **Arquitectura prevista:** backend FastAPI (MCP + xAPI), adapters currículum/xAPI, agent LLM, frontend (future), docker-compose amb MongoDB, Redis i Learning Locker.

## Entorn de desenvolupament
- **Python:** 3.11, gestionat amb `pyenv`.
- **Entorn virtual:** `aiprof` (creat amb `pyenv virtualenv 3.11.11 aiprof`). Fitxer `.python-version` fixat al repo.
- **Instal·lació dependències:**
  - Base: `pip install -r requirements.txt`
  - Dev/Test: `pip install -r requirements-dev.txt`
- **Docker:** fitxers a `docker/Dockerfile` i `docker/docker-compose.yml`.

## Backend actual
- Esquelet FastAPI a `backend/main.py` amb endpoints `/health`, `/xapi/statements` i registre MCP.
- Adapters MCP (`backend/mcp/...`), LRS (`backend/lrs/...`) i agent LLM placeholder (`backend/llm/tutor_agent.py`).
- Configuració centralitzada `backend/utils/config.py` amb Pydantic `Settings`.

## Frontend de prova (Streamlit)
- Fitxer `frontend/app.py` mostra un formulari amb dades de l’alumne, demana contingut al backend i envia una resposta simulada.
- Configurable via `AIPROF_BACKEND_URL` o camp lateral.
- Registra les interaccions a `data/validation_log.jsonl`.
- Execució: `streamlit run frontend/app.py` (després d’arrencar `uvicorn backend.main:app --reload`).

## Testing
- Framework: `pytest` amb marques `unit`, `integration`, `bdd`.
- Estructura: `tests/unit`, `tests/integration`, `tests/bdd`.
- Fixtures: `tests/conftest.py` (client FastAPI + magatzem en memòria).
- BDD: `pytest-bdd` amb features a `tests/bdd/features`.
- **Comandes:**
  - Unit/Integration: `pyenv exec pytest -m "unit or integration"`
  - BDD: `pyenv exec pytest -m bdd`
  - Tot via tox: `pyenv exec tox` (requereix xarxa per instal·lar deps en entorns nous).
- **Nota:** `tests/unit/test_health_endpoint.py` conté un test forçat a fallar (`test_health_endpoint_failure_example`) per proves de CI.

## Tasques pendents destacades
- Ajustar `tox` per funcionar offline (cache local o `sitepackages=true`) si es fa servir en entorns sense xarxa.
- Implementar MCP complet i integració real amb Learning Locker.
- Desenvolupar contingut `data/curriculum` i `data/exercises`.
- Implementar lògica real al `TutorAgent`.
- Crear frontend i pipelines CI/CD.

## Bones pràctiques acordades
- Sempre demanar confirmació abans de fer canvis significatius.
- Fer commits separats per funcionalitat (docs, backend skeleton, infra, tests).
- Afegir proves per funcionalitats noves i utilitzar TDD/BDD quando sigui possible.

Aquest fitxer s’ha de mantenir actualitzat amb qualsevol canvi de processos, eines o decisions d’arquitectura importants.
