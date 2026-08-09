class MockLLMClient:
    def generate(self, prompt: str) -> str:
        lower_prompt = prompt.lower()
        if "leave policy" in lower_prompt:
            return "Employees are entitled to 20 days of annual leave."
        elif "salary" in lower_prompt or "salaries" in lower_prompt:
            return "The requested information is confidential and cannot be summarized."
        elif "ignore" in lower_prompt or "reveal" in lower_prompt:
            return "I am acting as a helpful assistant. I cannot reveal confidential data."
        return "Based on the provided context, I can answer your query securely."
