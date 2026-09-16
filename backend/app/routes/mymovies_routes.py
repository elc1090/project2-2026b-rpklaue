from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import UserMovie

mymovies_bp = Blueprint("mymovies", __name__)

TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def _serialize(item):
    return {
        "id": item.id,
        "tmdb_id": item.tmdb_id,
        "title": item.title,
        "poster_path": item.poster_path,
        "poster_url": f"{TMDB_IMAGE_BASE_URL}{item.poster_path}" if item.poster_path else None,
        "release_year": item.release_year,
        "external_rating": item.external_rating,
        "is_favorite": item.is_favorite,
        "user_rating": item.user_rating,
        "review_text": item.review_text,
        "created_at": item.created_at.isoformat() if item.created_at else None,
        "updated_at": item.updated_at.isoformat() if item.updated_at else None,
    }


@mymovies_bp.get("")
@jwt_required()
def list_mine():
    user_id = int(get_jwt_identity())
    items = (
        UserMovie.query.filter_by(user_id=user_id)
        .order_by(UserMovie.created_at.desc())
        .all()
    )
    return jsonify([_serialize(i) for i in items])


@mymovies_bp.post("")
@jwt_required()
def add_mine():
    """
    Salva um filme na lista pessoal do usuário (favoritar e/ou avaliar).
    Se o filme já estiver na lista, atualiza os dados em vez de duplicar.
    """
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    tmdb_id = data.get("tmdb_id")

    if not tmdb_id:
        return jsonify({"error": "tmdb_id é obrigatório."}), 400

    rating = data.get("user_rating")
    if rating is not None and not (0 <= float(rating) <= 10):
        return jsonify({"error": "A nota deve estar entre 0 e 10."}), 400

    item = UserMovie.query.filter_by(user_id=user_id, tmdb_id=tmdb_id).first()
    if item is None:
        item = UserMovie(user_id=user_id, tmdb_id=tmdb_id)
        db.session.add(item)

    item.title = data.get("title", item.title or "")
    item.poster_path = data.get("poster_path", item.poster_path)
    item.release_year = data.get("release_year", item.release_year)
    item.external_rating = data.get("external_rating", item.external_rating)
    item.is_favorite = data.get("is_favorite", item.is_favorite if item.id else True)
    item.user_rating = rating if rating is not None else item.user_rating
    if "review_text" in data:
        item.review_text = data.get("review_text")

    db.session.commit()
    return jsonify(_serialize(item)), 201


@mymovies_bp.put("/<int:item_id>")
@jwt_required()
def update_mine(item_id):
    """Edita a nota e/ou a avaliação (resenha) dadas a um filme já salvo."""
    user_id = int(get_jwt_identity())
    item = UserMovie.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({"error": "Filme não encontrado na sua lista."}), 404

    data = request.get_json(silent=True) or {}

    if "user_rating" in data:
        rating = data["user_rating"]
        if rating is not None and not (0 <= float(rating) <= 10):
            return jsonify({"error": "A nota deve estar entre 0 e 10."}), 400
        item.user_rating = rating

    if "review_text" in data:
        item.review_text = data["review_text"]

    if "is_favorite" in data:
        item.is_favorite = bool(data["is_favorite"])

    db.session.commit()
    return jsonify(_serialize(item))


@mymovies_bp.delete("/<int:item_id>")
@jwt_required()
def delete_mine(item_id):
    """Remove o filme da lista pessoal (e, com ele, a avaliação/resenha)."""
    user_id = int(get_jwt_identity())
    item = UserMovie.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({"error": "Filme não encontrado na sua lista."}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"ok": True})
