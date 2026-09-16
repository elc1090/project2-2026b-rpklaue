import os

from dotenv import load_dotenv

load_dotenv()  # carrega o arquivo .env antes de importar a app (que lê os.environ)

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
