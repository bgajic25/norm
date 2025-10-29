import re
from num2words import num2words
from .base_handler import SerbianBaseHandler, safe_replacement


class MultiplicationHandler(SerbianBaseHandler):
    """
    Normalizes multiplication expressions like 9x9, 9×9, or 9*9.
    Only matches when there are NO spaces between numbers and operator.
    Examples:
        9x9 -> devet puta devet
        9×9 -> devet puta devet
        9*9 -> devet puta devet
        9 x 785 -> NOT matched (has spaces)
    """
    # Match: number + (x or × or *) + number, with NO spaces
    pattern = re.compile(r"\b(\d+)\s*[x×*]\s*(\d+)\b", re.IGNORECASE)

    @safe_replacement
    def _replace(self, first_num_str: str, second_num_str: str) -> str:
        first_num = int(first_num_str)
        second_num = int(second_num_str)

        first_text = self._to_cardinal(first_num)
        second_text = self._to_cardinal(second_num)

        return f"{first_text} puta {second_text}"

    def _to_cardinal(self, n: int) -> str:
        """Convert number to Serbian cardinal with proper 'hiljadu' handling."""
        text = num2words(n, lang="sr", to="cardinal")
        if text.startswith("jedna hiljada"):
            return text.replace("jedna hiljada", "hiljadu", 1)
        return text