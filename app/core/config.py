class Settings:
    """Application configuration settings."""
    DB_URL = "postgresql+psycopg://user:pass@db:5432/ads"  # ✅ MUST HAVE /ads
    REDIS_URL = "redis://redis:6379/0"

settings = Settings()