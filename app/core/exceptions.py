class LanguageNotSupportedError(Exception):
    """Raised when a normalizer strategy for a given language is not found."""
    def __init__(self, lang_code: str):
        self.lang_code = lang_code
        super().__init__(f"Language '{lang_code}' is not supported.")