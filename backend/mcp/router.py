from fastapi import APIRouter, HTTPException, Query

from backend.llm.tutor_agent import TutorAgent
from backend.mcp.adapters.xapi_adapter import XAPIAdapter
from backend.mcp.schemas import (
    AssessmentResult,
    CurriculumModule,
    CurriculumResponse,
    ExerciseAssessmentRequest,
    ExerciseGenerationRequest,
    ExercisePayload,
)
from backend.mcp.services.curriculum_service import (
    CurriculumNotFoundError,
    CurriculumService,
)

mcp_router = APIRouter()


@mcp_router.get(
    "/curriculum/{level}",
    response_model=CurriculumResponse,
    summary="Retrieve curriculum modules for a level (optionally by subject).",
)
async def get_curriculum(
    level: str,
    subject: str | None = Query(
        default=None,
        description="Optional subject filter, e.g. 'castellà' o 'matemàtiques'.",
    ),
) -> CurriculumResponse:
    service = CurriculumService()
    try:
        modules = service.list_modules(level, subject)
    except CurriculumNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return CurriculumResponse(level=level, subject=subject, modules=list(modules))


@mcp_router.get(
    "/curriculum/{level}/modules/{module_id}",
    response_model=CurriculumModule,
    summary="Retrieve a single curriculum module by ID.",
)
async def get_curriculum_module(level: str, module_id: str) -> CurriculumModule:
    service = CurriculumService()
    try:
        module = service.get_module(level, module_id)
    except CurriculumNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return module


@mcp_router.post("/xapi/forward")
async def forward_statement(statement: dict) -> dict[str, str]:
    adapter = XAPIAdapter()
    adapter.forward_statement(statement)
    return {"status": "forwarded"}


@mcp_router.post(
    "/exercises/generate",
    response_model=ExercisePayload,
    summary="Generate an exercise prompt for the specified curriculum module.",
)
async def generate_exercise(
    request: ExerciseGenerationRequest,
) -> ExercisePayload:
    service = CurriculumService()
    agent = TutorAgent()
    try:
        module = service.get_module(request.level, request.module_id)
    except CurriculumNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return agent.generate_exercise(level=request.level, module=module)


@mcp_router.post(
    "/exercises/assess",
    response_model=AssessmentResult,
    summary="Assess a learner answer for a previously generated exercise.",
)
async def assess_exercise(
    request: ExerciseAssessmentRequest,
) -> AssessmentResult:
    agent = TutorAgent()
    return agent.assess_answer(exercise=request.exercise, answer=request.answer)
