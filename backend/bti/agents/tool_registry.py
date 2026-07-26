from typing import Callable, Dict, Any

class AgentToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any], description: str):
        self.tools[name] = func
        return {"name": name, "description": description, "registered": True}

    def describe(self):
        return {name: getattr(func, "__doc__", "") or "Cognira BTI agent tool" for name, func in self.tools.items()}

    def call(self, name: str, **kwargs):
        if name not in self.tools:
            return {"error": f"Tool {name} not registered"}
        return self.tools[name](**kwargs)
