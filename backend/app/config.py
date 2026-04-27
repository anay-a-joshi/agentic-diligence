from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM
    gemini_api_key: str = ""

    # SEC
    sec_user_agent: str = "DiligenceAI Research contact@example.com"

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    allowed_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
