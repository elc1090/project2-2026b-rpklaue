from flask import Blueprint, jsonify, request

from ..services import tmdb_service as tmdb

movie_bp = Blueprint("movies", __name__)


@movie_bp.get("/search")
def search():
    """
    Busca/lista filmes western.

    - Sem parâmetro "q": retorna os westerns mais populares (para o usuário
      simplesmente navegar/"browsing" quando abre a página).
    - Com "q": busca por texto e filtra para o gênero Western.
    """
    query = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    try:
        data = tmdb.search_westerns(query, page=page) if query else tmdb.discover_westerns(page=page)
    except tmdb.TMDBError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify(
        {
            "page": data.get("page", page),
            "total_pages": data.get("total_pages", 1),
            "results": [tmdb.format_movie_summary(m) for m in data.get("results", [])],
        }
    )


@movie_bp.get("/<int:tmdb_id>")
def detail(tmdb_id):
    """Detalhes de um filme específico: sinopse, elenco, gêneros, duração, nota externa."""
    try:
        data = tmdb.get_movie_details(tmdb_id)
    except tmdb.TMDBError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify(tmdb.format_movie_detail(data))
