from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class settings(BaseSettings):
    DATABASE_URL: str
    SMTP_PORT: int
    SMTP_SERVER: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str
    SECRET_KEY:str
    ALGORITHM :str
    ACCESS_TOKEN_EXPIRE:int
    class Config:
        env_file = ".env"

settings = settings()
