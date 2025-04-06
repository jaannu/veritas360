class MultiAgentFramework:
    def __init__(self, agents): self.agents = agents

    def run(self, task):
        result = {}
        for agent in self.agents:
            result[agent.__class__.__name__] = agent.think(task)
        return result
