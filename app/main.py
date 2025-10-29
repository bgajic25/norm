from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import api_router
from app.normalizers.factory import normalizer_factory
from app.normalizers.sr.strategy import SerbianNormalizerStrategy
from app.normalizers.en.strategy import EnglishNormalizerStrategy
from app.normalizers.de.strategy import GermanNormalizerStrategy


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Registering normalizer strategies...")
    normalizer_factory.register("sr", SerbianNormalizerStrategy)
    normalizer_factory.register("en", EnglishNormalizerStrategy)
    normalizer_factory.register("de", GermanNormalizerStrategy)
    print("Registration complete.")
    yield
    print("Shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.APP_NAME}"}