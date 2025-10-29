import re
from num2words import num2words
from .base_handler import GermanBaseHandler, safe_replacement


class GermanRomanNumeralHandler(GermanBaseHandler):
    """
    Normalizes Roman numerals from I to M (1 to 1000).
    Only matches complete Roman numeral words, not partial matches.

    Examples:
    - I → eins
    - V → fünf
    - X → zehn
    - XX → zwanzig
    - M → eintausend
    """

    # Strict pattern: word boundary + valid Roman numeral + word boundary
    # This prevents matching empty strings or partial Roman numerals
    pattern = re.compile(
        r"\b([IVXLCDM]+)\b",
        re.IGNORECASE
    )

    def __init__(self):
        self._roman_numerals = self._load_json_data("roman_numerals.json")

    @safe_replacement
    def _replace(self, roman_str: str) -> str:
        # Normalize to uppercase for lookup
        roman_upper = roman_str.upper()

        # Check if it's actually a valid Roman numeral
        num = self._roman_numerals.get(roman_upper)

        if num is None:
            # Not a valid Roman numeral, return original
            raise ValueError(f"'{roman_str}' is not a supported Roman numeral.")

        return num2words(num, lang="de", to="cardinal")