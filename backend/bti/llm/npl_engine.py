from typing import Dict, Any
from bti.llm.narrative_forge import NarrativeForge

class NPLEngine:
    """Backward-compatible Narrative Processing Layer facade for source tree compliance."""
    def __init__(self):
        self.forge = NarrativeForge()

    def narrate(self, evidence: Dict[str, Any], persona: str = "compliance_officer") -> Dict[str, Any]:
        return self.forge.generate(evidence, persona)
