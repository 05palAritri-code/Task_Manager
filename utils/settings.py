from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_CONNECTION : str
    SECRET_KEY : str
    ALGORITHM : str
    EXP_TIME: int

    model_config = SettingsConfigDict(env_file=".env" , extra="ignore")

settings = Settings()

# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DB_CONNECTION: str | None = None
#     SECRET_KEY: str | None = None
#     ALGORITHM: str = "HS256"
#     EXP_TIME: int = 3600

#     def validate(self):
#         if not self.DB_CONNECTION or not self.SECRET_KEY:
#             raise ValueError("Missing required environment variables")

# settings = Settings()
# settings.validate()

