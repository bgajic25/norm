from app.normalizers.base import NormalizerStrategy, NormalizationHandler
from .rules.date_handler import DateHandler
from .rules.currency_handler import CurrencyHandler
from .rules.year_handler import YearHandler
from .rules.roman_numeral_handler import RomanNumeralHandler
from .rules.measurement_handler import MeasurementHandler
from .rules.multiplication_handler import MultiplicationHandler
from .rules.brand_handler import BrandHandler
from .rules.number_handler import NumberHandler


class SerbianNormalizerStrategy(NormalizerStrategy):
    """
    The concrete strategy for normalizing Serbian text.
    It constructs and executes a chain of normalization handlers.
    """
    def __init__(self):
        self._chain_head: NormalizationHandler = self._build_chain()

    def _build_chain(self) -> NormalizationHandler:
        """
        Instantiates and links the handlers in the correct processing order.
        """
        date_handler = DateHandler()
        currency_handler = CurrencyHandler()
        brand_handler = BrandHandler()
        year_handler = YearHandler()
        roman_numeral_handler = RomanNumeralHandler()
        measurement_handler = MeasurementHandler()
        multiplication_handler = MultiplicationHandler()
        number_handler = NumberHandler()

        date_handler.set_next(currency_handler) \
            .set_next(brand_handler) \
            .set_next(year_handler) \
            .set_next(roman_numeral_handler) \
            .set_next(measurement_handler) \
            .set_next(multiplication_handler) \
            .set_next(number_handler)

        return date_handler

    def normalize(self, text: str) -> str:
        """
        Executes the normalization chain on the input text.
        """
        return self._chain_head.handle(text)