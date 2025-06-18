from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-8b-8192"
    SERP_API_KEY: str
    QDRANT_API_KEY: str
    QDRANT_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
