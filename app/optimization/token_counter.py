class TokenCounter:
    def __init__(self):
        # A simple approximation: 1 token ~= 4 characters for English text
        self.chars_per_token = 4

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        return len(text) // self.chars_per_token
