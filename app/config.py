from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_HOSTNAME: str
    DB_PORT: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_USERNAME: str 
    
    class Config:
        env_file = ".env" 

settings = Settings()
