"""FastAPI Application Setup."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.db.database import db_manager
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database is initialized
    db_manager.init_database(force_reload=False)
    yield
    # Shutdown logic if any

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Agente de atendimento e inteligência conversacional para a Empório da Música.",
        lifespan=lifespan
    )

    # Enable CORS for frontend clients (React/Vite)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app

app = create_app()

