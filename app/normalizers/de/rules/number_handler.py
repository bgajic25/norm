import re
from num2words import num2words
from .base_handler import GermanBaseHandler, safe_replacement


class GermanNumberHandler(GermanBaseHandler):
    """
    Normalizes generic numbers, including integers and decimals.
    This should be the LAST handler in the chain for numbers.
    Handles both German format (1.000,50) and simple formats (1000, 1000.50)
    """

    pattern = re.compile(r"\b(\d+(?:[.,]\d+)?)\b")

    @safe_replacement
    def _replace(self, num_str: str) -> str:
        # Use inherited _parse_amount() from base_handler
        whole_val, dec_val = self._parse_amount(num_str)

        if whole_val == 0 and dec_val == 0:
            return "null"

        if dec_val > 0:
            whole_text = self._to_cardinal(whole_val)
            dec_text = self._to_cardinal(dec_val)
            return f"{whole_text} Komma {dec_text}"
        else:
            return self._to_cardinal(whole_val)

    def _to_cardinal(self, n: int) -> str:
        return num2words(n, lang="de", to="cardinal")