"""
Camada de integração com a API pública do TMDB (The Movie Database).

Toda a comunicação com o TMDB acontece aqui, no backend — a chave de API
nunca é exposta ao frontend. Isso também centraliza o filtro pelo gênero
Western (id 37 no TMDB) e a formatação dos dados que o frontend consome.

Documentação: https://developer.themoviedb.org/reference/intro/getting-started
"""

import os

import requests

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
WESTERN_GENRE_ID = 37
REQUEST_TIMEOUT_SECONDS = 10


class TMDBError(Exception):
    """Erro ao comunicar com a API do TMDB."""


def _api_key():
    key = os.environ.get("TMDB_API_KEY")
    if not key:
        raise TMDBError(
            "TMDB_API_KEY não configurada. Crie uma conta gratuita em "
            "themoviedb.org e defina a variável de ambiente TMDB_API_KEY."
        )
    return key


def _get(path, params=None, language="pt-BR"):
    """
    Faz a chamada HTTP ao TMDB.

    `language=None` pula o parâmetro de idioma de propósito: o TMDB, quando
    recebe "language=pt-BR", às vezes devolve poster_path/backdrop_path como
    nulo para filmes que não têm uma imagem específica cadastrada nesse
    idioma — o que é comum em westerns clássicos. Sem o parâmetro, ele
    devolve o pôster "canônico" do filme, que praticamente sempre existe.
    """
    params = dict(params or {})
    params["api_key"] = _api_key()
    if language:
        params["language"] = language
    try:
        response = requests.get(f"{TMDB_BASE_URL}{path}", params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise TMDBError(f"Falha ao consultar o TMDB: {exc}") from exc


def discover_westerns(page=1):
    """
    Lista filmes western populares (usado quando não há busca por texto).

    Sem "language" aqui de propósito, para garantir que o pôster sempre
    venha preenchido (ver nota em `_get`). Título/sinopse ficam no idioma
    original nesta listagem — não é um problema porque o card só mostra
    título, ano e nota, e o título de filme raramente muda de um idioma
    para o outro.
    """
    return _get(
        "/discover/movie",
        {"with_genres": WESTERN_GENRE_ID, "sort_by": "popularity.desc", "page": page},
        language=None,
    )


def search_westerns(query, page=1):
    """Busca filmes por texto e filtra o resultado para o gênero Western."""
    data = _get("/search/movie", {"query": query, "page": page}, language=None)
    data["results"] = [
        movie for movie in data.get("results", [])
        if WESTERN_GENRE_ID in (movie.get("genre_ids") or [])
    ]
    return data


def get_movie_details(tmdb_id):
    """
    Detalhes completos de um filme, incluindo elenco (credits).

    Aqui SIM pedimos pt-BR, porque a sinopse e os nomes de gênero aparecem
    inteiros na tela de detalhes e vale a pena estarem em português. Se por
    causa disso o pôster vier nulo, buscamos de novo sem idioma só para
    recuperar a imagem (uma chamada extra, e só quando necessário).
    """
    data = _get(f"/movie/{tmdb_id}", {"append_to_response": "credits"}, language="pt-BR")
    if not data.get("poster_path"):
        fallback = _get(f"/movie/{tmdb_id}", language=None)
        data["poster_path"] = fallback.get("poster_path")
    return data


def format_movie_summary(movie):
    """Formato resumido, usado nas listagens (busca e 'meus filmes')."""
    poster_path = movie.get("poster_path")
    return {
        "tmdb_id": movie.get("id"),
        "title": movie.get("title") or movie.get("original_title"),
        "poster_path": poster_path,
        "poster_url": f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None,
        "release_year": (movie.get("release_date") or "")[:4],
        "external_rating": movie.get("vote_average"),
        "synopsis": movie.get("overview"),
    }


def format_movie_detail(movie):
    """Formato completo, usado na tela de detalhes de um filme."""
    poster_path = movie.get("poster_path")
    credits = movie.get("credits") or {}
    cast = [
        {"name": person.get("name"), "character": person.get("character")}
        for person in (credits.get("cast") or [])[:10]
    ]
    return {
        "tmdb_id": movie.get("id"),
        "title": movie.get("title") or movie.get("original_title"),
        "poster_path": poster_path,
        "poster_url": f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None,
        "release_year": (movie.get("release_date") or "")[:4],
        "genres": [genre.get("name") for genre in (movie.get("genres") or [])],
        "synopsis": movie.get("overview"),
        "external_rating": movie.get("vote_average"),
        "runtime_minutes": movie.get("runtime"),
        "cast": cast,
    }
