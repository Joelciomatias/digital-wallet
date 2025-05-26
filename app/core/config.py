from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
