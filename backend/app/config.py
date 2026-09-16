import os


class Config:
    """Configuração da aplicação, lida a partir de variáveis de ambiente."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES_HOURS = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24))

    # Aceita SQLite (dev), PostgreSQL ou MySQL (prod), conforme a DATABASE_URL.
    _db_url = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    if _db_url.startswith("postgres://"):
        # Render/Heroku às vezes fornecem a URL com o prefixo antigo "postgres://",
        # mas o SQLAlchemy moderno exige "postgresql://".
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")

    _origins = os.environ.get("CORS_ORIGINS", "*")
    CORS_ORIGINS = [o.strip() for o in _origins.split(",")] if _origins != "*" else "*"
