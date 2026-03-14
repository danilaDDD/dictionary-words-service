from fastapi import FastAPI

from app.lifespan import lifespan
from app.middlewares.error_middleware import ErrorMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.logging import initialize_logger
from app.routers.word_router import word_router

app = FastAPI(lifespan=lifespan)

app.add_middleware(ErrorMiddleware)
app.add_middleware(LoggingMiddleware)

app.include_router(word_router)

initialize_logger(app)

