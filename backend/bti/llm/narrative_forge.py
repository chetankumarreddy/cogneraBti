from typing import Any, Dict
from bti.llm.prompt_chain import PromptChain
from bti.llm.gemini_agent import GeminiNarrativeAgent
from bti.llm.local_llm import LocalLLMAdapter
from bti.llm.story_guardian import StoryGuardian

class NarrativeForge:
    def __init__(self):
        self.gemini = GeminiNarrativeAgent()
        self.local = LocalLLMAdapter()
        self.guardian = StoryGuardian()

    def runtime_status(self) -> Dict[str, Any]:
        return {
            "engine": "Narrative Forge",
            "gemini": self.gemini.status(),
            "local_llm": self.local.status(),
            "prompt_chain": "persona + evidence + control + confidence chain",
            "story_guardian": "enabled"
        }

    def generate(self, evidence: Dict[str, Any], persona: str = "compliance_officer") -> Dict[str, Any]:
        prompt = PromptChain(persona, evidence).build()
        gemini_result = self.gemini.generate(prompt)
        text = gemini_result.get("text") or self.local.generate_template(evidence, persona)
        tx_id = evidence.get("transaction", {}).get("txn_id")
        confidence = float(evidence.get("risk", {}).get("confidence", 0.0))
        guardian = self.guardian.validate(text, confidence, [tx_id] if tx_id else [])
        return {
            "persona": persona,
            "text": text,
            "llm_provider": "gemini" if gemini_result.get("used") else "local_template",
            "gemini_result": gemini_result,
            "prompt_payload": prompt,
            "guardian": guardian
        }
