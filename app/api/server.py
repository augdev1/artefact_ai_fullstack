"""FastAPI Application Setup and Static Frontend Server."""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.db.database import db_manager
from app.api.routes import router

STATIC_DIR = settings.BASE_DIR / "app" / "static"

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

    # Enable CORS for local development and clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include REST API endpoints
    app.include_router(router)

    # Mount static assets directory
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

        @app.get("/", include_in_schema=False)
        async def serve_index():
            """Serve the responsive React Single Page Application."""
            return FileResponse(str(STATIC_DIR / "index.html"))

    return app

app = create_app()
