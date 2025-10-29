import functools
import json
import logging
import re
from pathlib import Path
from typing import Any, Callable, Match

from app.normalizers.base import NormalizationHandler

logger = logging.getLogger(__name__)

SR_DATA_PATH = Path(__file__).parent.parent / "data"


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


class SerbianBaseHandler(NormalizationHandler):
    """
    A base class for all Serbian normalization handlers, providing
    common utilities and enforcing the chain of responsibility pattern.
    """

    pattern: re.Pattern = re.compile("")

    @staticmethod
    def _load_json_data(filename: str) -> Any:
        """Loads data from a JSON file in the Serbian data directory."""
        try:
            with open(SR_DATA_PATH / filename, "r", encoding="utf-8") as f:
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
        FLEXIBLE amount parser that detects BOTH US and German formats:
        - US format: 1,234.56 (comma=thousands, dot=decimal)
        - German format: 1.234,56 (dot=thousands, comma=decimal)
        - Serbian uses German format: 1.234,56

        Detection rule: The RIGHTMOST separator determines format
        - If rightmost is dot (.) with ≤2 digits after → US decimal
        - If rightmost is comma (,) with ≤2 digits after → German/Serbian decimal
        - If rightmost has 3+ digits after it → it's thousands separator

        Returns: (whole_part, decimal_part)
        """
        if not amount_str:
            return 0, 0

        clean = amount_str.replace(" ", "").replace("\u00A0", "")

        # Find rightmost separator positions
        last_comma_pos = clean.rfind(',')
        last_dot_pos = clean.rfind('.')

        # Determine rightmost separator
        rightmost_pos = max(last_comma_pos, last_dot_pos)

        if rightmost_pos == -1:
            # No separators at all
            try:
                return int(clean), 0
            except ValueError:
                logger.warning(f"Could not parse amount: {amount_str}")
                return 0, 0

        # Get digits after rightmost separator
        digits_after_rightmost = len(clean) - rightmost_pos - 1

        # If exactly 2 digits after rightmost → it's definitely decimal
        if digits_after_rightmost == 2:
            decimal_sep = clean[rightmost_pos]
            thousands_sep = ',' if decimal_sep == '.' else '.'

            # Remove thousands separators
            clean = clean.replace(thousands_sep, '')

            # Split on decimal separator
            parts = clean.split(decimal_sep)
            whole = int(parts[0]) if parts[0] else 0
            decimal = int(parts[1]) if len(parts) > 1 and parts[1] else 0
            return whole, decimal

        # If 1 digit after rightmost → decimal with single digit (e.g., "5.0")
        elif digits_after_rightmost == 1:
            decimal_sep = clean[rightmost_pos]
            thousands_sep = ',' if decimal_sep == '.' else '.'
            clean = clean.replace(thousands_sep, '')
            parts = clean.split(decimal_sep)
            whole = int(parts[0]) if parts[0] else 0
            decimal = int(parts[1]) if len(parts) > 1 and parts[1] else 0
            return whole, decimal

        # If 3 digits after rightmost → it's thousands separator
        elif digits_after_rightmost == 3:
            # Remove ALL separators - they're all thousands separators
            clean = clean.replace(',', '').replace('.', '')
            try:
                return int(clean), 0
            except ValueError:
                logger.warning(f"Could not parse amount: {amount_str}")
                return 0, 0

        # More than 3 digits after → definitely thousands
        elif digits_after_rightmost > 3:
            clean = clean.replace(',', '').replace('.', '')
            try:
                return int(clean), 0
            except ValueError:
                logger.warning(f"Could not parse amount: {amount_str}")
                return 0, 0

        # Fallback: just try to parse
        else:
            try:
                clean_no_sep = clean.replace(',', '').replace('.', '')
                return int(clean_no_sep), 0
            except ValueError:
                logger.warning(f"Could not parse amount: {amount_str}")
                return 0, 0

    def _to_cardinal(self, n: int) -> str:
        """Convert number to Serbian words"""
        from num2words import num2words
        return num2words(n, lang="sr")