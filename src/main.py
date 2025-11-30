from fastapi import FastAPI
from src.api.v1 import phishing_router, analysis_router, healthcheck
from src.core.container import Container

container = Container()
app = FastAPI(title="Guardião Digital", version="0.1.0")

app.include_router(healthcheck.router, prefix="/api/v1")
app.include_router(phishing_router.router, prefix="/api/v1")
app.include_router(analysis_router.router, prefix="/api/v1")
