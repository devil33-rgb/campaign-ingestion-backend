from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

print("DB URL:", settings.DB_URL)
engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(bind=engine)

