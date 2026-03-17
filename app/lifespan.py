from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from app.db.session_manager import SessionManager, get_session_manager
from settings.settings import load_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = load_settings()
    app.state.session = SessionManager(app.state.settings).start()
    yield
    await app.state.session.close()
    app.state.settings = None
    app.state.session = None


