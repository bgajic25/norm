import re
from num2words import num2words
from .base_handler import EnglishBaseHandler, safe_replacement

class EnglishRomanNumeralHandler(EnglishBaseHandler):
    """Normalizes Roman numerals from I to XX."""
    pattern = re.compile(
        r"\b((?:X{1,2}|IX|IV|V|X|I{1,3}|VI{0,3}|XI{1,2}|XIV|XV|XVI{0,3}|XIX|XX))\b"
    )

    def __init__(self):
        self._roman_to_num = self._load_json_data("roman_numerals.json")

    @safe_replacement
    def _replace(self, roman_str: str) -> str:
        num = self._roman_to_num.get(roman_str)
        if num is None:
            raise ValueError(f"'{roman_str}' is not a supported Roman numeral.")
        return num2words(num, lang="en", to="cardinal")
