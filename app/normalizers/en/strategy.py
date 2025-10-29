from app.normalizers.base import NormalizerStrategy, NormalizationHandler

from .rules.date_handler import EnglishDateHandler
from .rules.currency_handler import EnglishCurrencyHandler
from .rules.roman_numeral_handler import EnglishRomanNumeralHandler
from .rules.measurement_handler import EnglishMeasurementHandler
from .rules.multiplication_handler import EnglishMultiplicationHandler
from .rules.number_handler import EnglishNumberHandler


class EnglishNormalizerStrategy(NormalizerStrategy):
    """
    The concrete strategy for normalizing English text.
    It constructs and executes a chain of normalization handlers.
    """

    def __init__(self):
        self._chain_head: NormalizationHandler = self._build_chain()

    def _build_chain(self) -> NormalizationHandler:
        """
        Build the chain of responsibility in correct order:
        1. DateHandler - MUST BE FIRST (before numbers break dates)
        2. CurrencyHandler - Handle €, $, £, etc.
        3. MultiplicationHandler - Handle × (before general numbers)
        4. MeasurementHandler - Handle inch, feet, km/h, etc.
        5. RomanNumeralHandler - Handle I, II, III, etc.
        6. NumberHandler - Handle remaining numbers
        """
        date_handler = EnglishDateHandler()
        currency_handler = EnglishCurrencyHandler()
        multiplication_handler = EnglishMultiplicationHandler()
        measurement_handler = EnglishMeasurementHandler()
        roman_numeral_handler = EnglishRomanNumeralHandler()
        number_handler = EnglishNumberHandler()

        # Build chain correctly - FIX: Remove duplicate return statement
        date_handler.set_next(currency_handler) \
            .set_next(multiplication_handler) \
            .set_next(measurement_handler) \
            .set_next(roman_numeral_handler) \
            .set_next(number_handler)

        return date_handler  # ✓ Single return - CORRECT

    def normalize(self, text: str) -> str:
        """
        Executes the normalization chain on the input text.
        """
        return self._chain_head.handle(text)