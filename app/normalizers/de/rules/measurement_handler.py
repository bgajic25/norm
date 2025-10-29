import re
from typing import Dict
from num2words import num2words
from .base_handler import GermanBaseHandler, safe_replacement


class GermanMeasurementHandler(GermanBaseHandler):
    """
    Normalizes measurement units into German spoken form.
    Examples:
    - 7.5 l/100km → sieben Komma fünf Liter pro hundert Kilometer
    - 120 m² → einhundertzwanzig Quadratmeter
    - 25°C → fünfundzwanzig Grad Celsius
    """

    pattern = re.compile("")

    def __init__(self) -> None:
        data = self._load_json_data("measurements.json")
        self._units_map: Dict[str, str] = data.get("units", {})

        if self._units_map:
            # Sort by length (longest first) to match compound units like "km/h" before "km"
            sorted_units = sorted(self._units_map.keys(), key=len, reverse=True)
            unit_pattern = "|".join(re.escape(unit) for unit in sorted_units)

            # Build regex: number (with German format) + optional space + unit
            self.pattern = re.compile(
                rf"(\d{{1,3}}(?:[.,]\d{{3}})*(?:[.,]\d{{1,2}})?|\d+(?:[.,]\d{{1,2}})?)[\u00A0\s]*({unit_pattern})(?=\s|$|[^\w])",
                re.MULTILINE
            )
        else:
            # No units found, disable this handler
            self.pattern = re.compile(r"(?!x)")

    @safe_replacement
    def _replace(self, number: str, unit: str) -> str:
        normalized_unit = self._units_map.get(unit)

        if normalized_unit is None:
            raise ValueError(f"Unsupported measurement unit: {unit}")

        if number:
            # Use inherited _parse_amount() from base_handler
            whole_val, dec_val = self._parse_amount(number)

            if whole_val > 0:
                whole_text = self._to_cardinal(whole_val)

                if dec_val > 0:
                    dec_text = self._to_cardinal(dec_val)
                    number_text = f"{whole_text} Komma {dec_text}"
                else:
                    number_text = whole_text

                return f"{number_text} {normalized_unit}"
            elif dec_val > 0:
                dec_text = self._to_cardinal(dec_val)
                return f"{dec_text} {normalized_unit}"

        return normalized_unit

    def _to_cardinal(self, n: int) -> str:
        return num2words(n, lang="de", to="cardinal")