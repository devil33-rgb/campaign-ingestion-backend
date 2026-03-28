from fastapi import FastAPI
from app.api.routes import router
from app.db.models import Base
from app.db.session import engine

app = FastAPI(title="Campaign Ingestion API",
    description="Handles CSV ingestion, processing, and campaign analytics",
    version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(router)