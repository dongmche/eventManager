import random

class CodeGenerator:
    def __init__(self, code_length=8):
        self.code_length = code_length

    def generate_code(self) -> str:
        """
        Generates a numeric code of the specified length.
        The code consists of digits only (0-9).
        """
        digits = '0123456789'  # Only digits
        code = ''.join(random.choices(digits, k=self.code_length))
        return code

