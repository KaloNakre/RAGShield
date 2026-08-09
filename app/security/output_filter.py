class OutputFilter:
    def __init__(self):
        self.sensitive_patterns = ["social security", "credit card", "salary information"]

    def is_safe(self, text: str) -> bool:
        lower_text = text.lower()
        for pattern in self.sensitive_patterns:
            if pattern in lower_text:
                return False
        return True
