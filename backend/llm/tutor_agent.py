from typing import Any

from backend.utils.config import get_settings


class TutorAgent:
    """LLM-driven tutor placeholder that prepares prompts and responses."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._model = self._settings.llm_model

    def generate_exercise(self, topic: str, level: str) -> dict[str, Any]:
        # TODO: integrate with real LLM provider (OpenAI, local model, etc.).
        return {
            "topic": topic,
            "level": level,
            "prompt": (
                f"Describe a concept about {topic} suitable for {level} grade "
                f"students and provide a practice exercise."
            ),
        }

    def assess_answer(self, exercise: dict[str, Any], answer: str) -> dict[str, Any]:
        # TODO: call the LLM for evaluation logic.
        return {
            "exercise": exercise,
            "answer": answer,
            "feedback": "Assessment pending LLM integration.",
            "score": None,
        }
