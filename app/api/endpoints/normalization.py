from fastapi import APIRouter, HTTPException, status, Path
from app.core.exceptions import LanguageNotSupportedError
from app.normalizers.factory import normalizer_factory
from app.schemas.normalization import NormalizationRequest, NormalizationResponse

router = APIRouter()

@router.post(
    "/{lang}/normalize",
    response_model=NormalizationResponse,
    summary="Normalize text for a specific language",
)
def normalize_text(
    request: NormalizationRequest,
    lang: str = Path(
        ...,
        min_length=2,
        max_length=2,
        regex="^[a-z]{2}$",
        examples=["sr"],
        description="Two-letter lowercase language code (ISO 639-1)."
    ),
):
    """
    Normalizes the provided text according to the rules for the specified language.

    - **lang**: The language code for the normalization rules to apply.
    - **request body**: A JSON object containing the `text` to be normalized.

    Returns the normalized text. If the language is not supported,
    a 404 error is returned.
    """
    try:
        strategy = normalizer_factory.get_strategy(lang)
        normalized_text = strategy.normalize(request.text)
        return NormalizationResponse(normalized_text=normalized_text)
    except LanguageNotSupportedError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )