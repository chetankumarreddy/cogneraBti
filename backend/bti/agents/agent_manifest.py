COGNIRA_AGENT_MANIFEST = {
    "name": "cognira-bti-investigation-agent",
    "display_name": "Cognira BTI Investigation Agent",
    "runtime": "local_or_gemini_agent_platform",
    "description": "Evidence-grounded blockchain transaction intelligence agent for compliance, audit, financial crime and FCA-style narratives.",
    "tools": [
        "analyse_transaction",
        "generate_narrative",
        "retrieve_context",
        "explain_model",
        "export_evidence_pack"
    ],
    "guardrails": [
        "Never assume unknown entities",
        "Use supplied evidence only",
        "Human review required below confidence threshold",
        "Preserve evidence lineage"
    ]
}
