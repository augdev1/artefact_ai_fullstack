"""Application Main Entrypoint."""

import uvicorn
from app.config import settings
from app.api.server import app

def main():
    print(f"Starting {settings.APP_NAME} on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )

if __name__ == "__main__":
    main()

