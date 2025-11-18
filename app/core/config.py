from dotenv import load_dotenv
from pydantic import BaseSettings
load_dotenv()

class settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = settings()
