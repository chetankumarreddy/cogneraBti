try:
    from google.adk import Agent
except Exception:  # ADK optional for hackathon package
    Agent = None

INSTRUCTION = """
You are Cognira BTI Investigation Agent. Use only supplied evidence and registered tools.
Generate UK regulatory tone narratives for compliance, audit, financial crime and FCA-style workflows.
Never assume unknown entities. If confidence is insufficient, state: I don’t know. Human review required.
"""

def analyse_transaction(txn_id: str) -> dict:
    from bti.agents.cognira_agent import CogniraBTIAgent
    return CogniraBTIAgent().analyse_transaction(txn_id)

def retrieve_context(query: str) -> dict:
    from bti.agents.cognira_agent import CogniraBTIAgent
    return CogniraBTIAgent().retrieve_context(query)

if Agent:
    root_agent = Agent(
        name="cognira_bti_investigation_agent",
        model="gemini-flash-latest",
        instruction=INSTRUCTION,
        tools=[analyse_transaction, retrieve_context],
    )
else:
    root_agent = None
