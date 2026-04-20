import os


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    secret_key: str = os.getenv("SECRET_KEY", "shelfsense-dev-secret-key")
    token_ttl_seconds: int = int(os.getenv("TOKEN_TTL_SECONDS", str(60 * 60 * 12)))


settings = Settings()
