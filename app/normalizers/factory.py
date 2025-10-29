from typing import Dict, Type
from app.core.exceptions import LanguageNotSupportedError
from app.normalizers.base import NormalizerStrategy


class NormalizerFactory:
    """
    Factory for creating and managing language-specific normalizer strategies.
    This class follows the Singleton pattern to ensure a single registry.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NormalizerFactory, cls).__new__(cls)
            cls._instance._strategies: Dict[str, Type[NormalizerStrategy]] = {}
            cls._instance._cache: Dict[str, NormalizerStrategy] = {}
        return cls._instance

    def register(self, lang_code: str, strategy_class: Type[NormalizerStrategy]) -> None:
        """Registers a new normalizer strategy class for a given language code."""
        self._strategies[lang_code] = strategy_class

    def get_strategy(self, lang_code: str) -> NormalizerStrategy:
        """
        Retrieves an instance of the normalizer strategy for the given language code.
        Instances are cached for performance.

        Args:
            lang_code: The two-letter language code (e.g., 'sr').

        Returns:
            An instance of the NormalizerStrategy.

        Raises:
            LanguageNotSupportedError: If no strategy is registered for the lang_code.
        """
        if lang_code in self._cache:
            return self._cache[lang_code]

        strategy_class = self._strategies.get(lang_code)
        if not strategy_class:
            raise LanguageNotSupportedError(lang_code)
        
        instance = strategy_class()
        self._cache[lang_code] = instance
        return instance

normalizer_factory = NormalizerFactory()