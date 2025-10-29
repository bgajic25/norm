import re
from num2words import num2words
from .base_handler import SerbianBaseHandler, safe_replacement


class DateHandler(SerbianBaseHandler):
    """Normalizes dates in DD.MM.YYYY. format."""
    pattern = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\.?\b")

    def __init__(self):
        self._months_gen = self._load_json_data("months.json")
        self._ordinals_gen = self._load_json_data("ordinals.json")

    @safe_replacement
    def _replace(self, day_str: str, month_str: str, year_str: str) -> str:
        d, m, y = int(day_str), int(month_str), int(year_str)

        if not (1 <= m <= 12 and 1 <= d <= 31):
            raise ValueError(f"Invalid date: D={d}, M={m}")

        day_text = self._ordinals_gen.get(str(d))
        month_text = self._months_gen.get(str(m))

        if day_text is None or month_text is None:
            raise ValueError(f"Day '{d}' or month '{m}' out of range for lookup.")

        year_text = self._to_year(y)
        return f"{day_text} {month_text} {year_text}."

    def _to_year(self, y: int) -> str:
        text = num2words(y, lang="sr", to="year")
        if text.startswith("jedna hiljada"):
            return text.replace("jedna hiljada", "hiljadu", 1)
        return text