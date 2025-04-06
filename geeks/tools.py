import requests

class OllamaLLM:
    def run(self, prompt):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False}
            )
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"❌ Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"❌ Exception: {str(e)}"


class WebScraperTool:
    def run(self, query): return f"Web data for: {query}"


class APIClientTool:
    def run(self, query): return f"API results for: {query}"


class CustomMLModel:
    def run(self, query): return f"ML Insights for: {query}"
