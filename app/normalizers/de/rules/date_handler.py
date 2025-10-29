import re
from num2words import num2words
from .base_handler import GermanBaseHandler, safe_replacement


class GermanDateHandler(GermanBaseHandler):
    """Normalizes dates in DD.MM.YYYY. format (EU standard)."""

    pattern = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\.?\b")

    def __init__(self):
        self._months = self._load_json_data("months.json")
        self._ordinals = self._load_json_data("ordinals.json")

    @safe_replacement
    def _replace(self, day_str: str, month_str: str, year_str: str) -> str:
        d, m, y = int(day_str), int(month_str), int(year_str)

        # Validate date ranges
        if not (1 <= m <= 12 and 1 <= d <= 31):
            raise ValueError(f"Invalid date: D={d}, M={m}")

        # Get ordinal form (e.g., "1." → "ersten", "12." → "zwölften")
        day_text = self._ordinals.get(str(d))
        month_text = self._months.get(str(m))

        if day_text is None or month_text is None:
            raise ValueError(f"Day '{d}' or month '{m}' out of range for lookup.")

        # Convert year to German words
        year_text = num2words(y, lang="de")

        return f"{day_text} {month_text} {year_text}"