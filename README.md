# AIProf

AIProf és un projecte per construir un professor virtual intel·ligent per a alumnat d’ESO i més endavant. L’objectiu és oferir exercicis personalitzats, correccions guiades i seguiment detallat del progrés mitjançant l’estàndard xAPI, tot integrant el Model Context Protocol (MCP) per gestionar context educatiu i recursos externs.

## Objectius clau
- Generar i corregir preguntes i exercicis adaptats al nivell de l’alumne.
- Emprar xAPI per registrar cada activitat en un Learning Record Store (LRS).
- Integrar MCP per obtenir context acadèmic i recursos curriculars.
- Oferir una interfície senzilla per a l’alumne (fase posterior).

## Arquitectura prevista
```
AIProf/
├── backend/
│   ├── main.py                # servidor FastAPI (MCP + endpoints xAPI)
│   ├── mcp/
│   │   ├── router.py          # lògica de connexió MCP
│   │   └── adapters/
│   │       ├── xapi_adapter.py
│   │       └── curriculum_adapter.py
│   ├── lrs/
│   │   ├── local_store.py     # registre xAPI local (fitxer/SQLite)
│   │   └── remote_store.py    # connector cap al LRS (Learning Locker)
│   ├── llm/
│   │   └── tutor_agent.py     # lògica del professor IA
│   └── utils/
│       └── config.py
├── frontend/
│   └── app.py                 # interfície d’alumne (Streamlit o React)
├── docker/
│   ├── docker-compose.yml     # Mongo 8 + Redis + Learning Locker + LRS
│   └── Dockerfile             # backend
├── data/
│   ├── exercises/
│   ├── curriculum/
│   └── xapi_log.json
├── requirements.txt
├── .env.example
└── README.md
```

## Infraestructura
- `docker-compose.yml` amb MongoDB 8, Redis 6, Learning Locker i serveis auxiliars amb volums persistents (`./volumes/`).
- Desplegament flexible en entorns locals o distribuïts (producció).
- Backend basat en FastAPI amb connectors MCP i endpoints xAPI.

## Funcionalitats principals
- **Backend MCP**: gestiona les peticions educatives, accedeix a recursos i centralitza el context.
- **xAPI statements**: endpoint `/xapi/statements` per emmagatzemar activitats a l’LRS (local o remot).
- **Adapters modulars**: integracions per al currículum i pel registre d’activitat.
- **Tutor Agent LLM**: genera exercicis, corregeix respostes i envia informes al LRS.
- **Frontend educatiu**: interfície de l’alumne amb xat i feedback (pròxima fase).

## Stack tecnològic
- Python 3.11, FastAPI, LangChain/LlamaIndex, MCP.
- MongoDB 8, Redis 6, Learning Locker (LRS).
- Docker/Docker Compose per a l’orquestració.
- Streamlit o React per al frontend.

## Configuració inicial
1. Crea un fitxer `.env` basat en `.env.example` amb credencials d’APIs i serveis.
2. Executa `docker compose up -d` dins de `docker/` per arrencar MongoDB, Redis i Learning Locker.
3. Instal·la dependències del backend: `pip install -r requirements.txt`.
4. Inicia el backend: `uvicorn backend.main:app --reload`.
5. Llança el frontend (quan estigui disponible) segons la tecnologia triada.

### Prova conceptual amb Streamlit
1. Activa l’entorn `pyenv activate aiprof` i instal·la les dependències: `pip install -r requirements-dev.txt`.
2. En una terminal, arrenca el backend: `uvicorn backend.main:app --reload`.
3. En una altra terminal, llança la demo: `streamlit run frontend/app.py`.
4. Escull el nivell, l’assignatura disponible i el mòdul que vulguis treballar, redacta la resposta i envia.  
   - Les peticions MCP es fan via `/mcp/curriculum/{nivell}` i `/mcp/exercises/*`.  
   - Les respostes s’envien a `/xapi/statements` i es registren a `data/xapi_log.jsonl` i `data/validation_log.jsonl`.

## Full de ruta immediat
1. Construir l’esquelet complet del projecte i crear els mòduls principals.
2. Implementar `backend/main.py` amb endpoints MCP i xAPI.
3. Desenvolupar `lrs/local_store.py` i `lrs/remote_store.py`.
4. Crear `llm/tutor_agent.py` amb integració OpenAI o model local.
5. Preparar `README.md`, `.env.example`, `requirements.txt` i scripts de desplegament.
6. Configurar GitHub Actions per a tests i validacions CI/CD.

## Contribució
Les propostes de millora i issues són benvingudes. Mantén un estil de codi coherent, afegeix tipatge i documenta qualsevol API nova. Abans d’enviar canvis:
- Executa els tests i formatadors necessaris.
- Actualitza la documentació si cal.

## Llicència
Defineix la llicència del projecte (per exemple, MIT, Apache-2.0) a mesura que s’avanci en el desenvolupament.
