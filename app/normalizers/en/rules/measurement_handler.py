import re
from typing import Dict
from num2words import num2words
from .base_handler import EnglishBaseHandler, safe_replacement


class EnglishMeasurementHandler(EnglishBaseHandler):
    """Normalizes measurement units into English spoken form."""

    pattern = re.compile("")

    def __init__(self) -> None:
        data = self._load_json_data("measurements.json")
        self._units_map: Dict[str, str] = data.get("units", {})

        if self._units_map:
            sorted_units = sorted(self._units_map.keys(), key=len, reverse=True)
            unit_pattern = "|".join(re.escape(unit) for unit in sorted_units)

            # Jednostavan pattern koji hvata sve
            self.pattern = re.compile(
                rf"(?P<number>\d{{1,3}}(?:[.,]\d{{3}})*(?:[.,]\d{{1,2}})?|\d+(?:[.,]\d{{1,2}})?)\s*(?P<unit>{unit_pattern})(?=\s|$|[^\w])"
            )
        else:
            self.pattern = re.compile(r"(?!x)")

    @safe_replacement
    def _replace(self, number: str, unit: str) -> str:
        normalized_unit = self._units_map.get(unit)
        if normalized_unit is None:
            raise ValueError(f"Unsupported measurement unit: {unit}")

        if number:
            # Koristi novi parsing
            whole_val, dec_val = self._parse_amount(number)

            if whole_val > 0:
                whole_text = self._to_cardinal(whole_val)
                if dec_val > 0:
                    dec_text = self._to_cardinal(dec_val)
                    number_text = f"{whole_text} point {dec_text}"
                else:
                    number_text = whole_text

                return f"{number_text} {normalized_unit}"
            else:
                return normalized_unit
        return normalized_unit

    def _to_cardinal(self, n: int) -> str:
        return num2words(n, lang="en", to="cardinal")
