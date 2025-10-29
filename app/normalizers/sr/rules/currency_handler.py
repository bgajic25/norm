import re
from num2words import num2words
from .base_handler import SerbianBaseHandler, safe_replacement


class CurrencyHandler(SerbianBaseHandler):
    """Normalizes currency formats like €1.234,56, 1.234,56€, 11.230 €, or 500 RSD."""
    # Universal currency pattern - matches ANY number format with currency context
    pattern = re.compile(
        r"(?P<prefix_symbol>€|\$|£|¥|₹|₿)[\u00A0\s]*"
        r"(?P<prefix_amount>\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)\b"
        r"|"
        r"(?P<suffix_amount>\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)[\u00A0\s]*"
        r"(?P<suffix_code>USD\b|EUR\b|GBP\b|JPY\b|CHF\b|BTC\b|[€$£¥₹₿])"
    )

    def __init__(self):
        self._currency_names = self._load_json_data("currencies.json")
        self._symbol_map = {
            "€": "EUR", "$": "USD", "£": "GBP", "¥": "JPY", "₹": "INR", "₿": "BTC",
            "RSD": "RSD", "EUR": "EUR", "USD": "USD", "GBP": "GBP",
            "JPY": "JPY", "INR": "INR", "CHF": "CHF", "BTC": "BTC"
        }

    @safe_replacement
    def _replace(
            self,
            prefix_symbol: str | None,
            prefix_amount: str | None,
            suffix_amount: str | None,
            suffix_code: str | None,
    ) -> str:
        symbol = prefix_symbol or suffix_code
        amount_str = prefix_amount or suffix_amount

        if not symbol or not amount_str:
            raise ValueError("Invalid currency match")

        code = self._symbol_map[symbol]
        names = self._currency_names[code]

        whole_val, dec_val = self._parse_amount(amount_str)  # NOVO

        # Handle zero amounts
        if whole_val == 0 and dec_val == 0:
            return f"nula {names[1]}"

        result_parts = []

        # Handle whole amount
        if whole_val > 0:
            whole_text = self._to_cardinal(whole_val)
            major_name = names[0] if whole_val % 10 == 1 and whole_val % 100 != 11 else names[1]
            result_parts.append(f"{whole_text} {major_name}")

        # Handle decimal amount
        if dec_val > 0:
            dec_text = self._to_cardinal(dec_val)
            minor_name = names[2] if dec_val % 10 == 1 and dec_val % 100 != 11 else names[3]
            result_parts.append(f"{dec_text} {minor_name}")

        # Join with "i" for Serbian
        if len(result_parts) == 2:
            return f"{result_parts[0]} i {result_parts[1]}"
        else:
            return result_parts[0]

    def _split_amount(self, s: str) -> tuple[int, int]:
        """Split amount into whole and decimal parts (Serbian uses , for decimals)"""
        clean = s.replace(".", "")  # Remove thousand separators
        parts = clean.split(",")
        whole = int(parts[0])
        decimal = int(parts[1]) if len(parts) > 1 else 0
        return whole, decimal

    def _to_cardinal(self, n: int) -> str:
        text = num2words(n, lang="sr", to="cardinal")
        if text.startswith("jedna hiljada"):
            return text.replace("jedna hiljada", "hiljadu", 1)
        return text
