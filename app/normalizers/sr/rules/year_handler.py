import re
from num2words import num2words
from .base_handler import SerbianBaseHandler

class YearHandler(SerbianBaseHandler):
    """
    Normalizes years. It handles multiple cases:
    1. "2023. godine" -> "dve hiljade dvadeset treće godine"
    2. "2021. godište" -> "dve hiljade dvadeset prvo godište"
    3. "2021." -> "dve hiljade dvadeset prva."
    4. "2021" -> "dve hiljade dvadeset jedan"
    """

    def __init__(self):
        self._ordinals_neuter = self._load_json_data("ordinals_neuter.json")
        self._ordinals_feminine = self._load_json_data("ordinals_feminine.json")

    def handle(self, text: str) -> str:
        text = re.sub(
            r"\b(19\d{2}|20\d{2}|2100)\.\s*godine\b",
            lambda m: self._replace_genitive(m.group(1)),
            text
        )
        text = re.sub(
            r"\b(19\d{2}|20\d{2}|2100)\.\s*(godište|izdanje|kolo)\b",
            lambda m: self._replace_neuter(m.group(1), m.group(2)),
            text
        )
        text = re.sub(
            r"\b(19\d{2}|20\d{2}|2100)\.(?!\s*(godine|godište|izdanje|kolo))",
            lambda m: self._replace_feminine(m.group(1)),
            text
        )
        text = re.sub(
            r"\b(19\d{2}|20\d{2}|2100)(?!\.)(?!\d)\b",
            lambda m: self._replace_nominative(m.group(1)),
            text
        )
        if self._next_handler:
            return self._next_handler.handle(text)
        return text

    def _replace_genitive(self, year_str: str) -> str:
        try:
            year = int(year_str)
            year_text_genitive = self._to_year_genitive(year)
            return f"{year_text_genitive} godine"
        except Exception as e:
            return f"{year_str}. godine"

    def _replace_neuter(self, year_str: str, noun: str) -> str:
        try:
            year = int(year_str)
            year_text = self._to_year_neuter(year)
            return f"{year_text} {noun}"
        except Exception as e:
            return f"{year_str}. {noun}"

    def _replace_feminine(self, year_str: str) -> str:
        try:
            year = int(year_str)
            year_text = self._to_year_feminine(year)
            return f"{year_text}."
        except Exception as e:
            return f"{year_str}."

    def _replace_nominative(self, year_str: str) -> str:
        try:
            year = int(year_str)
            year_text = num2words(year, lang="sr", to="year")
            if year_text.startswith("jedna hiljada"):
                year_text = year_text.replace("jedna hiljada", "hiljadu", 1)
            return year_text
        except Exception as e:
            return year_str

    def _to_year_feminine(self, y: int) -> str:
        if y >= 2000:
            result = "dve hiljade"
            remainder = y % 1000
            if remainder > 0:
                result += f" {self._get_ordinal_feminine_suffix(remainder)}"
            else:
                result = "dvehiljadita"
        elif y >= 1900:
            result = "hiljadu devetsto"
            remainder = y % 100
            if remainder == 0:
                result += "ta"
            else:
                result += f" {self._get_ordinal_feminine_suffix(remainder)}"
        else:
            return num2words(y, lang='sr', to='ordinal')

        return result

    def _to_year_neuter(self, y: int) -> str:
        if y >= 2000:
            result = "dve hiljade"
            remainder = y % 1000
            if remainder > 0:
                result += f" {self._get_ordinal_neuter_suffix(remainder)}"
            else:
                result = "dvehiljadito"
        elif y >= 1900:
            result = "hiljadu devetsto"
            remainder = y % 100
            if remainder == 0:
                result += "to"
            else:
                result += f" {self._get_ordinal_neuter_suffix(remainder)}"
        else:
            return num2words(y, lang='sr', to='ordinal')

        return result

    def _to_year_genitive(self, y: int) -> str:
        if y >= 2000:
            if y == 2000:
                return "dvehiljadite"

            result = "dve hiljade"
            remainder = y % 1000
            if remainder > 0:
                result += f" {self._get_ordinal_genitive_suffix(remainder)}"
            return result
        elif y >= 1900:
            result = "hiljadu devetsto"
            remainder = y % 100
            if remainder == 0:
                return result + "te"
            else:
                result += f" {self._get_ordinal_genitive_suffix(remainder)}"
            return result

        return num2words(y, lang='sr', to='ordinal')

    def _get_ordinal_feminine_suffix(self, n: int) -> str:
        if n <= 31 and str(n) in self._ordinals_feminine:
            return self._ordinals_feminine[str(n)]

        tens = n // 10
        ones = n % 10

        ones_feminine = {
            1: "prva", 2: "druga", 3: "treća", 4: "četvrta",
            5: "peta", 6: "šesta", 7: "sedma", 8: "osma", 9: "deveta"
        }
        tens_names = {
            2: "dvadeset", 3: "trideset", 4: "četrdeset", 5: "pedeset",
            6: "šezdeset", 7: "sedamdeset", 8: "osamdeset", 9: "devedeset"
        }
        tens_feminine = {
            1: "deseta", 2: "dvadeseta", 3: "trideseta", 4: "četrdeseta",
            5: "pedeseta", 6: "šezdeseta", 7: "sedamdeseta",
            8: "osamdeseta", 9: "devedeseta"
        }

        if ones == 0:
            return tens_feminine[tens]
        else:
            return f"{tens_names[tens]} {ones_feminine[ones]}"

    def _get_ordinal_neuter_suffix(self, n: int) -> str:
        if n <= 31 and str(n) in self._ordinals_neuter:
            return self._ordinals_neuter[str(n)]

        tens = n // 10
        ones = n % 10

        ones_neuter = {
            1: "prvo", 2: "drugo", 3: "treće", 4: "četvrto",
            5: "peto", 6: "šesto", 7: "sedmo", 8: "osmo", 9: "deveto"
        }
        tens_names = {
            2: "dvadeset", 3: "trideset", 4: "četrdeset", 5: "pedeset",
            6: "šezdeset", 7: "sedamdeset", 8: "osamdeset", 9: "devedeset"
        }
        tens_neuter = {
            1: "deseto", 2: "dvadeseto", 3: "trideseto", 4: "četrdeseto",
            5: "pedeseto", 6: "šezdeseto", 7: "sedamdeseto",
            8: "osamdeseto", 9: "devedeseto"
        }

        if ones == 0:
            return tens_neuter[tens]
        else:
            return f"{tens_names[tens]} {ones_neuter[ones]}"

    def _get_ordinal_genitive_suffix(self, n: int) -> str:
        tens = n // 10
        ones = n % 10

        ones_genitive = {
            1: "prve", 2: "druge", 3: "treće", 4: "četvrte",
            5: "pete", 6: "šeste", 7: "sedme", 8: "osme", 9: "devete"
        }
        teens_genitive = {
            11: "jedanaeste", 12: "dvanaeste", 13: "trinaeste",
            14: "četrnaeste", 15: "petnaeste", 16: "šesnaeste",
            17: "sedamnaeste", 18: "osamnaeste", 19: "devetnaeste"
        }
        tens_names = {
            2: "dvadeset", 3: "trideset", 4: "četrdeset", 5: "pedeset",
            6: "šezdeset", 7: "sedamdeset", 8: "osamdeset", 9: "devedeset"
        }
        tens_genitive = {
            1: "desete", 2: "dvadesete", 3: "tridesete", 4: "četrdesete",
            5: "pedesete", 6: "šezdesete", 7: "sedamdesete",
            8: "osamdesete", 9: "devedesete"
        }

        if 1 <= n <= 9:
            return ones_genitive[n]
        if n == 10:
            return tens_genitive[1]
        if 11 <= n <= 19:
            return teens_genitive[n]
        if 20 <= n <= 99:
            if ones == 0:
                return tens_genitive[tens]
            else:
                return f"{tens_names[tens]} {ones_genitive[ones]}"

        return num2words(n, lang='sr', to='ordinal')