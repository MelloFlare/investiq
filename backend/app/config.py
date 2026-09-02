from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = ""  # loaded from .env — your Supabase connection string
    MARKET_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()