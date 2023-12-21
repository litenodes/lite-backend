from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from . import endpoints


def create_app() -> FastAPI:

    app = FastAPI()
    app.include_router(endpoints.router)
    return app


app = create_app()

FastAPICache.init(InMemoryBackend())
