# Rafael Penteado Klaue

## Ciência da Computação

## 1. Proposta

App web de busca e gerenciamento pessoal de filmes western, desenvolvido na modalidade A. O sistema permite cadastro e login de usuários com sessão mantida via token; navegação e busca de filmes do gênero western, exibindo capa, título, sinopse, gênero, ano, elenco e nota externa, com dados obtidos de uma API pública (TMDB — The Movie Database).

Cada usuário mantém sua própria lista de filmes favoritados, podendo atribuir uma nota, escrever uma avaliação, e editá-la ou excluí-la posteriormente. Os dados são persistentes, através de um banco de dados relacional, através de um backend próprio desenvolvido em Flask.

## 2. Parceria/cliente/usuário

Miguel Miron

## 3. Feedback/comentário da parceria/cliente/usuário

Criamos um grupo de WhatsApp para contato para trocarmos mensagens e imagens.

## 4. Processo

Eu tinha experiência prévia com Python, mas pouca com o uso de backend e de Flask. Algumas partes difíceis foram o pip travando ao instalar as dependências, e o `psycopg2-binary` não compilando.

Também precisei adaptar a escolha de banco de dados de NoSQL/MySQL para um banco relacional, e o campo "episódios", que não fazia sentido para filme.

## 5. Trechos de código

1. Em `mymovies_routes.py`, a lógica de "criar ou atualizar" (`UniqueConstraint("user_id", "tmdb_id")` + verificação antes de inserir) — evita duplicar o mesmo filme na lista do usuário sem precisar de lógica manual complexa.

2. Em `auth_routes.py`/rotas protegidas, o uso de `@jwt_required()` junto com `get_jwt_identity()` — mostra como a "sessão" funciona sem cookies, via token.

3. Em `movie-detail.js`, a lógica que decide entre POST (criar) e PUT (atualizar) dependendo se o filme já existe na lista (`entry`) — mostra controle de estado no frontend sem usar nenhum framework.

## 6. Linguagens e afins

* Python 3
* Flask
* SQLAlchemy (ORM)
* SQLite (ambiente de desenvolvimento)
* PostgreSQL (produção)
* HTML5
* CSS3
* JavaScript no frontend
* API pública TMDB (The Movie Database)

## 7. Ambiente de desenvolvimento

* **VS Code**, com as extensões:

  * Python (Microsoft)
  * Live Server (Ritwick Dey)
* Terminal integrado do VS Code (PowerShell, Windows)
* Venv (ambiente virtual do Python)
* Git e GitHub para versionamento
* Render (hospedagem do backend)
* Netlify (hospedagem do frontend)

## 8. Referências e créditos

* Documentação oficial do Flask — https://flask.palletsprojects.com/
* Documentação oficial do SQLAlchemy — https://docs.sqlalchemy.org/
* Documentação da API do TMDB — https://developer.themoviedb.org/reference/intro/getting-started
* Documentação do Flask-JWT-Extended — https://flask-jwt-extended.readthedocs.io/
