from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "Enclave"
    debug: bool = False

    # AI Providers
    llm_provider: str = "ollama"
    embedding_provider: str = "ollama"
    embedding_dimension: int = 768

    # Ollama
    ollama_host: str = "http://ollama:11434"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_gen_model: str = "llama3.2:3b"
    ollama_num_ctx: int = 4096
    ollama_timeout_seconds: int = 120

    # OpenAI
    openai_api_key: str = ""
    openai_embed_model: str = "text-embedding-3-small"
    openai_gen_model: str = "gpt-4o-mini"

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_gen_model: str = "claude-sonnet-4-6"

    # Database
    db_provider: str = "local"
    database_url: str = "postgresql+asyncpg://enclave:CHANGE_ME@db:5432/enclave"
    postgres_user: str = "enclave"
    postgres_password: str = "CHANGE_ME"
    postgres_db: str = "enclave"

    # Security
    secret_key: str = "CHANGE_ME_TO_RANDOM_64_CHAR_STRING_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    jwt_access_expiry_hours: int = 24
    jwt_refresh_expiry_days: int = 30

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Session
    session_ttl_days: int = 30
    session_purge_cron: str = "0 2 * * *"

    # Document editor
    enable_document_editor: bool = False
    onlyoffice_url: str = "http://onlyoffice:8443"
    onlyoffice_jwt_secret: str = "CHANGE_ME_ONLYOFFICE_SECRET"

    # Admin bootstrap
    admin_email: str = "admin@enclave.local"
    admin_password: str = "CHANGE_ME_ADMIN_PASSWORD"

    # Ingestion
    max_file_size_mb: int = 50
    supported_file_types: str = "pdf,docx,md,txt,csv"
    chunk_size_tokens: int = 400
    chunk_overlap_tokens: int = 50

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def supported_file_types_list(self) -> list[str]:
        return [t.strip() for t in self.supported_file_types.split(",") if t.strip()]


settings = Settings()
