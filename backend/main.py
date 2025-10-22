from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.lrs.local_store import LocalXAPIStore
from backend.mcp.router import mcp_router
from backend.utils.config import get_settings, Settings


class XAPIStatement(BaseModel):
    actor: dict
    verb: dict
    object: dict
    result: dict | None = None
    context: dict | None = None
    timestamp: str | None = None


app = FastAPI(title="AIProf Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_lrs(settings: Settings = Depends(get_settings)) -> LocalXAPIStore:
    return LocalXAPIStore(settings)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/xapi/statements", status_code=202)
async def ingest_xapi_statement(
    statement: XAPIStatement,
    lrs: LocalXAPIStore = Depends(get_lrs),
) -> dict[str, str]:
    lrs.save_statement(statement.dict())
    return {"status": "queued"}


app.include_router(mcp_router, prefix="/mcp", tags=["mcp"])
