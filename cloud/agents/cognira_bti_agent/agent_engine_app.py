from cloud.agents.cognira_bti_agent.agent import root_agent

class AgentEngineApp:
    def __init__(self):
        self.root_agent = root_agent
        self.name = "cognira-bti-investigation-agent"

    def query(self, message: str):
        return {"agent": self.name, "message": message, "mode": "local-placeholder"}
