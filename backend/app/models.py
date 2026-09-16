from datetime import datetime

from .extensions import db


class User(db.Model):
    """Um usuário cadastrado no app."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    movies = db.relationship(
        "UserMovie", backref="user", cascade="all, delete-orphan", lazy="dynamic"
    )


class UserMovie(db.Model):
    """
    Relação entre um usuário e um filme (identificado pelo id do TMDB).

    Guarda apenas os dados necessários para exibir a lista pessoal sem
    precisar consultar a API externa de novo, além da nota e da avaliação
    dadas pelo usuário. Sinopse completa e elenco são buscados ao vivo na
    tela de detalhes do filme.
    """

    __tablename__ = "user_movies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    tmdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    poster_path = db.Column(db.String(255))
    release_year = db.Column(db.String(4))
    external_rating = db.Column(db.Float)

    is_favorite = db.Column(db.Boolean, default=False, nullable=False)
    user_rating = db.Column(db.Float)
    review_text = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "tmdb_id", name="uq_user_movie"),
    )
