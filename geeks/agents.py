class BaseAgent:
    def __init__(self, tools, db):
        self.tools = tools
        self.db = db

    def think(self, task): raise NotImplementedError


class UsecaseAgent(BaseAgent):
    def think(self, task):
        prompt = (
            "You are a banking expert. Understand the following use case in detail "
            "and explain how to implement a Customer 360 system in retail banking:\n\n"
            f"{task}"
        )
        res = self.tools[3].run(f"You are a banking expert. Please analyze and expand on the following use case:\n\n{task}\n\nExplain how a Customer 360 system would help solve this use case, including key benefits, required capabilities, and possible challenges."
)

        self.db.store("UsecaseAgent", task, res)
        return res


class SchemaAgent(BaseAgent):
    def think(self, task):
        prompt = (
            "Based on the following business use case, design a comprehensive data product schema "
            "including entities, attributes, and relationships:\n\n"
            f"{task}"
        )
        res = self.tools[3].run(
    f"Design a data product schema for the following business use case:\n\n{task}\n\nList the entities (e.g., Customer, Account), attributes (e.g., customer_id, transaction_date), and relationships. Format as a clear schema."
)
        self.db.store("SchemaAgent", task, res)
        return res


class MappingAgent(BaseAgent):
    def think(self, task):
        prompt = (
            "Given the business use case below, generate a source-to-target data mapping plan. "
            "Include example source systems, fields, and how they map to the data product schema:\n\n"
            f"{task}"
        )
        res = self.tools[3].run(
    f"For the business use case:\n\n{task}\n\nSuggest the source systems (like CRM, Core Banking) and generate a source-to-target mapping. Include field mappings and transformation logic where needed."
)

        self.db.store("MappingAgent", task, res)
        return res


class CertifierAgent(BaseAgent):
    def think(self, task):
        prompt = (
            "Certify the designed data product for the following use case. "
            "Define data quality checks, ingress/egress points, and how the data can be searched and validated:\n\n"
            f"{task}"
        )
        res = self.tools[3].run(
    f"Based on this Customer 360 data product:\n\n{task}\n\nDefine the ingress (data input) and egress (data output) flows, data quality rules, and how search/discovery can be enabled. Explain how to certify this data product against typical data governance standards."
)

        self.db.store("CertifierAgent", task, res)
        return res


class SentimentAgent(BaseAgent):
    def think(self, feedbacks):
        sentiments = []
        for fb in feedbacks:
            sentiment = "Positive" if "helpful" in fb or "resolved" in fb else "Negative"
            sentiments.append(f"{fb} → {sentiment}")
        result = "\n".join(sentiments)
        self.db.store("SentimentAgent", "Analyze sentiments", result)
        return result


class ChatbotAgent(BaseAgent):
    def think(self, queries):
        responses = []
        for q in queries:
            prompt = f"You are a customer support assistant. Answer this banking question:\n\n{q}"
            response = self.tools[3].run(prompt)
            responses.append(f"{q}\n→ {response}")
        result = "\n".join(responses)
        self.db.store("ChatbotAgent", "Customer queries", result)
        return result
