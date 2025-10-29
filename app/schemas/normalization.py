from pydantic import BaseModel, Field


class NormalizationRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        examples=["Tekst za normalizaciju, napisan 25.12.2023. godine, košta €1.234,56."],
        description="The input string to be normalized."
    )


class NormalizationResponse(BaseModel):
    normalized_text: str = Field(
        ...,
        examples=["Tekst za normalizaciju, napisan dvadeset petog decembra dve hiljade dvadeset treće. godine, košta hiljadu dvesta trideset četiri evra i pedeset šest centi."],
        description="The resulting normalized string."
    )