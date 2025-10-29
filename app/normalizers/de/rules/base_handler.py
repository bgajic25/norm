import functools
import json
import logging
import re
from pathlib import Path
from typing import Any, Callable, Match

from app.normalizers.base import NormalizationHandler

logger = logging.getLogger(__name__)

DE_DATA_PATH = Path(__file__).parent.parent / "data"


def safe_replacement(func: Callable[..., str]) -> Callable[..., str]:
    """
    Decorator to safely execute a replacement function for re.sub.
    If any exception occurs during the transformation, it logs the error
    and returns the original matched string, preventing a crash.
    """

    @functools.wraps(func)
    def wrapper(self, match: Match) -> str:
        original_string = match.group(0)
        try:
            return func(self, *match.groups())
        except Exception as e:
            logger.warning(
                f"Failed to normalize '{original_string}' using {self.__class__.__name__}. "
                f"Error: {e}. Returning original string."
            )
            return original_string

    return wrapper


class GermanBaseHandler(NormalizationHandler):
    """
    A base class for all German normalization handlers, providing
    common utilities and enforcing the chain of responsibility pattern.
    """

    pattern: re.Pattern = re.compile("")

    @staticmethod
    def _load_json_data(filename: str) -> Any:
        """Loads data from a JSON file in the German data directory."""
        try:
            with open(DE_DATA_PATH / filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load data from {filename}: {e}")
            return {}

    def handle(self, text: str) -> str:
        """
        Applies the handler's regex substitution and passes the result
        to the next handler in the chain.
        """
        normalized_text = self.pattern.sub(self._replace, text)
        return super().handle(normalized_text)

    def _replace(self, match: Match) -> str:
        """
        The core replacement logic to be implemented by subclasses.
        This method is what's called by re.sub for each match.
        It should be decorated with @safe_replacement.
        """
        raise NotImplementedError("Subclasses must implement the _replace method.")

    def _parse_amount(self, amount_str: str) -> tuple[int, int]:
        """
        Parse German format numbers: dot=thousands separator, comma=decimal separator
        Handles formats like: 1.234,56 (1234 euros 56 cents)

        Returns: (whole_part, decimal_part)
        """
        if not amount_str:
            return 0, 0

        clean = amount_str.replace(" ", "").replace("\u00A0", "")

        # Format: 11.000,50 (thousands + decimal)
        if re.match(r'^\d{1,3}(?:\.\d{3})*,\d{1,2}$', clean):
            clean = clean.replace(".", "")
            parts = clean.split(",")
            whole = int(parts[0])
            decimal = int(parts[1]) if len(parts) > 1 else 0
            return whole, decimal

        # Format: 11.000 (only thousands separator, no decimal - KEY FIX!)
        elif re.match(r'^\d{1,3}(?:\.\d{3})+$', clean):
            whole = int(clean.replace(".", ""))
            decimal = 0
            return whole, decimal

        # Format: 11,50 (only decimal, no thousands separator)
        elif ',' in clean:
            parts = clean.split(",")
            whole = int(parts[0])
            decimal = int(parts[1]) if len(parts) > 1 else 0
            return whole, decimal

        # Simple integer: 16000
        else:
            try:
                whole = int(clean)
                decimal = 0
                return whole, decimal
            except ValueError:
                logger.warning(f"Could not parse amount: {amount_str}")
                return 0, 0

    def _to_cardinal(self, n: int) -> str:
        """Convert number to German words (e.g., 123 → 'einhundertdreiundzwanzig')"""
        from num2words import num2words
        return num2words(n, lang="de")