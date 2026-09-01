from pydantic_settings import BaseSettings , SettingsConfigDict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = ROOT_DIR / ".env"

class Settings(BaseSettings):
    # database
    mongo_url : str
    database_name : str


    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    default_admin_email : str
    default_admin_password : str

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587

    SMTP_EMAIL: str = ""
    SMTP_PASSWORD: str = ""
    COMPANY_NAME: str = "Omnixa System"
    mail_from: str = ""

    RESEND_API_KEY: str = ""

    environment : str = "development"
    log_level: str = "INFO"
    log_file_path: str = "./logs/omni.log"

    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Omnixa"


    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(f"✅ Configuration loaded from environment")

settings = Settings()