from fastapi import APIRouter, HTTPException

from backend.mcp.adapters.curriculum_adapter import CurriculumAdapter
from backend.mcp.adapters.xapi_adapter import XAPIAdapter

mcp_router = APIRouter()


@mcp_router.get("/curriculum/{level}")
async def get_curriculum(level: str) -> dict:
    adapter = CurriculumAdapter()
    data = adapter.fetch_curriculum(level)
    if data is None:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    return {"level": level, "modules": data}


@mcp_router.post("/xapi/forward")
async def forward_statement(statement: dict) -> dict[str, str]:
    adapter = XAPIAdapter()
    adapter.forward_statement(statement)
    return {"status": "forwarded"}
