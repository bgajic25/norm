import re
from num2words import num2words
from .base_handler import EnglishBaseHandler, safe_replacement


class EnglishMultiplicationHandler(EnglishBaseHandler):
    """
    Normalizes multiplication expressions like 2556×1179, 5×100, 9x9, 9*9.
    Converts to: "two thousand five hundred fifty-six times one thousand one hundred seventy-nine"

    Supports:
    - 2556×1179 (with × symbol)
    - 2556x1179 (with x, case-insensitive)
    - 2556*1179 (with *)
    - Optional spaces: 2556 × 1179
    """

    # Match: number + (x or × or *) + number, with optional spaces
    pattern = re.compile(r"\b(\d+)\s*[x×*]\s*(\d+)\b", re.IGNORECASE)

    @safe_replacement
    def _replace(self, first_num_str: str, second_num_str: str) -> str:
        first_num = int(first_num_str)
        second_num = int(second_num_str)

        first_text = self._to_cardinal(first_num)
        second_text = self._to_cardinal(second_num)

        return f"{first_text} times {second_text}"

    def _to_cardinal(self, n: int) -> str:
        """Convert number to English cardinal."""
        return num2words(n, lang="en", to="cardinal")