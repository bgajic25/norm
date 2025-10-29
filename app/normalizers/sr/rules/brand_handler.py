import re
from typing import Dict
from .base_handler import SerbianBaseHandler, safe_replacement


class BrandHandler(SerbianBaseHandler):
    """Normalizes brand names for Serbian pronunciation."""

    pattern = re.compile("")

    def __init__(self) -> None:
        data = self._load_json_data("brands.json")
        self._brands_map: Dict[str, str] = data.get("brands", {})

        if self._brands_map:
            # Sort by length (longest first) to avoid partial matches
            sorted_brands = sorted(self._brands_map.keys(), key=len, reverse=True)
            # Escape special regex characters and create word boundary pattern
            brand_pattern = "|".join(re.escape(brand) for brand in sorted_brands)
            self.pattern = re.compile(
                rf"\b(?P<brand>{brand_pattern})\b",
                re.IGNORECASE
            )
        else:
            self.pattern = re.compile(r"(?!x)")

    @safe_replacement
    def _replace(self, brand: str) -> str:
        # Look up the brand (case-insensitive)
        normalized_brand = None
        for original_brand, pronunciation in self._brands_map.items():
            if original_brand.lower() == brand.lower():
                normalized_brand = pronunciation
                break

        if normalized_brand is None:
            raise ValueError(f"Unsupported brand: {brand}")

        return normalized_brand
