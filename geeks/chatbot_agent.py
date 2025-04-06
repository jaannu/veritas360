class ChatbotAgent:
    def __init__(self, tools, db):
        self.llm = tools[3]
        self.db = db

    def think(self, task):
        queries = [
            "How do I reset my password?",
            "Where can I find my bank statements?",
            "What is the interest rate for savings?"
        ]
        result = ""
        for q in queries:
            answer = self.llm.run(f"Answer this customer question: {q}")
            result += f"{q}\n→ {answer}\n"
        self.db.store("ChatbotAgent", task, result)
        print("[ChatbotAgent]:", result)
