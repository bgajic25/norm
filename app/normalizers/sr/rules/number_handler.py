import re

from num2words import num2words

from .base_handler import SerbianBaseHandler, safe_replacement


class NumberHandler(SerbianBaseHandler):
    """
    Normalizes generic numbers, including integers and decimals.
    This should be the LAST handler in the chain for numbers.
    Handles both Serbian format (1.000,50 or 1.000 for thousands) and decimals (50,50)
    """

    # FIXED: Match numbers with BOTH period (.) and comma (,) as separators
    pattern = re.compile(r"\b(\d+(?:[.,]\d+)*)\b")

    @safe_replacement
    def _replace(self, num_str: str) -> str:
        # Use inherited _parse_amount() from base_handler
        whole_val, dec_val = self._parse_amount(num_str)

        if whole_val == 0 and dec_val == 0:
            return "nula"

        if dec_val > 0:
            whole_text = self._to_cardinal(whole_val)
            dec_text = self._to_cardinal(dec_val)
            return f"{whole_text} zarez {dec_text}"
        else:
            return self._to_cardinal(whole_val)

    def _to_cardinal(self, n: int) -> str:
        text = num2words(n, lang="sr", to="cardinal")
        # Fix for "jedna hiljada" → "hiljadu" (accusative case)
        if text.startswith("jedna hiljada"):
            return text.replace("jedna hiljada", "hiljadu", 1)
        return text