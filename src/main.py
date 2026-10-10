from fastapi import FastAPI

from src.config import get_settings
from src.routers import ping

app = FastAPI(
    title="arXiv Paper Curator API",
    description="Personal arXiv CS.AI paper curator with RAG capabilities",
    version=get_settings().app_version,
    root_path="/api/v1",
)

app.include_router(ping.router)
