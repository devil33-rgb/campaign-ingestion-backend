from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from app.db.models import Base
import uuid

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="pending")
    processed = Column(Integer, default=0)
    rejected = Column(Integer, default=0)

    created_at = Column(TIMESTAMP, server_default=text("now()"))