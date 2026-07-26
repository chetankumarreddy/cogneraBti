import os
from typing import Any, Dict

class GeminiNarrativeAgent:
    """Optional Gemini Enterprise Agent Platform narrative adapter.

    The adapter is safe for hackathon mode: if google-cloud/Vertex libraries or credentials are
    unavailable, it returns a structured fallback response instead of failing the pipeline.
    """
    def __init__(self):
        self.project_id = os.getenv("BTI_GCP_PROJECT_ID", "")
        self.location = os.getenv("BTI_GCP_REGION", "europe-west2")
        self.model = os.getenv("BTI_GEMINI_MODEL", "gemini-2.5-pro")
        self.enabled = os.getenv("BTI_LLM_MODE", "mock") in {"gemini", "gemini_with_local_fallback"}

    def status(self) -> Dict[str, Any]:
        return {
            "provider": "gemini-enterprise-agent-platform",
            "enabled": self.enabled,
            "project_id_present": bool(self.project_id),
            "location": self.location,
            "model": self.model,
            "fallback": "local_template_narrative"
        }

    def generate(self, prompt_payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.enabled:
            return {"used": False, "reason": "Gemini mode not enabled", "text": ""}
        try:
            import vertexai  # type: ignore
            from vertexai.generative_models import GenerativeModel  # type: ignore
            vertexai.init(project=self.project_id, location=self.location)
            model = GenerativeModel(self.model)
            prompt = str(prompt_payload)
            response = model.generate_content(prompt)
            return {"used": True, "provider": "gemini", "text": response.text}
        except Exception as exc:
            return {"used": False, "provider": "gemini", "error": str(exc), "text": ""}
