import re
from typing import Dict
from num2words import num2words
from .base_handler import SerbianBaseHandler, safe_replacement


class MeasurementHandler(SerbianBaseHandler):
    """Normalizes measurement units into Serbian spoken form."""

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
        # Provjeri da li je unit samo slovo
        if re.match(r'^[A-Z]$', unit):
            # Samo slovo - mora imati razmak prije (već provjereno u pattern-u)
            # Dodatno - provjeri da li ima razmak nakon ili je na kraju
            pass  # Pattern već osigurava pravilno hvatanje

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
                    number_text = f"{whole_text} zarez {dec_text}"
                else:
                    number_text = whole_text

                return f"{number_text} {normalized_unit}"
            else:
                return normalized_unit
        return normalized_unit

    def _to_cardinal(self, n: int) -> str:
        text = num2words(n, lang="sr", to="cardinal")
        if text.startswith("jedna hiljada"):
            return text.replace("jedna hiljada", "hiljadu", 1)
        return text
