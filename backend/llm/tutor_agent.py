from __future__ import annotations

from backend.mcp.schemas import (
    AssessmentResult,
    CurriculumModule,
    ExercisePayload,
)
from backend.utils.config import get_settings


class TutorAgent:
    """LLM-driven tutor placeholder that prepares prompts and responses."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._model = self._settings.llm_model

    def generate_exercise(self, level: str, module: CurriculumModule) -> ExercisePayload:
        """Produce a scaffolded exercise based on curriculum metadata."""
        instructions = (
            "Respon en 3-4 frases clares. Pots oferir exemples i destacar conceptes clau."
        )
        prompt = (
            f"Unitat: {module.title}\n"
            f"Objectiu: {module.objective}\n"
            "Elabora una resposta a partir d'aquest enunciat d'exemple:\n"
            f"{module.example_exercise}\n"
            "Aporta una resposta personalitzada segons l'alumne."
        )
        return ExercisePayload(
            level=level,
            module_id=module.id,
            subject=module.subject,
            title=module.title,
            objective=module.objective,
            prompt=prompt,
            instructions=instructions,
        )

    def assess_answer(self, exercise: ExercisePayload, answer: str) -> AssessmentResult:
        """Return a lightweight heuristic assessment until an LLM is integrated."""
        cleaned = answer.strip()
        if not cleaned:
            return AssessmentResult(
                feedback=(
                    "Cal aportar una resposta perquè el tutor et pugui oferir feedback. "
                    "Repassa l'enunciat i intenta donar-hi una resposta detallada."
                ),
                score=0.0,
            )

        keywords = _extract_keywords(exercise.objective)
        coverage = (
            sum(1 for keyword in keywords if keyword in cleaned.lower()) / len(keywords)
            if keywords
            else 1.0
        )
        score = round(0.4 + 0.6 * coverage, 2)
        feedback = (
            "Bona resposta! Has tocat els conceptes principals."
            if coverage > 0.6
            else "La resposta és correcta però pots aprofundir una mica més en els conceptes clau."
        )
        return AssessmentResult(feedback=feedback, score=score)


def _extract_keywords(objective: str) -> list[str]:
    tokens = [
        word.strip(".,:;!?").lower()
        for word in objective.split()
        if len(word.strip(".,:;!?")) >= 6
    ]
    return tokens[:4]
