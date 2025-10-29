from abc import ABC, abstractmethod
from typing import Optional


class NormalizationHandler(ABC):
    """
    Abstract Base Class for a handler in a Chain of Responsibility.
    Each handler is responsible for a specific text normalization rule.
    """
    _next_handler: Optional["NormalizationHandler"] = None

    def set_next(self, handler: "NormalizationHandler") -> "NormalizationHandler":
        """
        Sets the next handler in the chain.

        Args:
            handler: The next handler instance.

        Returns:
            The handler instance, to allow for fluent chaining (e.g., h1.set_next(h2).set_next(h3)).
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, text: str) -> str:
        """
        Applies the handler's normalization rule and passes the text to the next handler.

        Args:
            text: The input text to normalize.

        Returns:
            The normalized text.
        """
        if self._next_handler:
            return self._next_handler.handle(text)
        return text


class NormalizerStrategy(ABC):
    """
    Abstract Base Class for a language-specific normalization strategy.
    This class encapsulates the entire normalization algorithm for one language.
    """
    @abstractmethod
    def normalize(self, text: str) -> str:
        """
        Performs normalization for a specific language.

        Args:
            text: The text to normalize.

        Returns:
            The fully normalized text.
        """
        pass