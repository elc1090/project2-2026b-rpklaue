from datetime import timedelta

from flask import Flask

from .config import Config
from .extensions import cors, db, jwt


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=app.config["JWT_ACCESS_TOKEN_EXPIRES_HOURS"]
    )

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from .routes.auth_routes import auth_bp
    from .routes.mymovies_routes import mymovies_bp
    from .routes.movie_routes import movie_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(movie_bp, url_prefix="/api/movies")
    app.register_blueprint(mymovies_bp, url_prefix="/api/my-movies")

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    @app.errorhandler(404)
    def not_found(_error):
        return {"error": "Rota não encontrada."}, 404

    with app.app_context():
        # Para este projeto de disciplina, criamos as tabelas automaticamente
        # ao iniciar (sem sistema de migrations, para simplificar o setup).
        db.create_all()

    return app
