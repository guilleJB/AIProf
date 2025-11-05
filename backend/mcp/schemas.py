from typing import Optional

from pydantic import BaseModel


class CurriculumModule(BaseModel):
    id: str
    title: str
    objective: str
    example_exercise: str
    subject: Optional[str] = None


class CurriculumResponse(BaseModel):
    level: str
    subject: Optional[str] = None
    modules: list[CurriculumModule]


class ExerciseGenerationRequest(BaseModel):
    level: str
    module_id: str


class ExercisePayload(BaseModel):
    level: str
    module_id: str
    title: str
    objective: str
    prompt: str
    instructions: str
    subject: Optional[str] = None


class ExerciseAssessmentRequest(BaseModel):
    exercise: ExercisePayload
    answer: str


class AssessmentResult(BaseModel):
    feedback: str
    score: Optional[float] = None
