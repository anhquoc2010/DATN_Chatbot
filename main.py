from fastapi import FastAPI
from app.api import router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
    application.include_router(router)
    return application

app = create_application()