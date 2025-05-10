from flask import Flask
from pathlib import Path
from app.core.routes import core_bp  # Importa o blueprint

# Define caminhos base
BASE_DIR = Path(__file__).resolve().parent

# Criação do app Flask
app = Flask(
    __name__,
    static_folder="app/static",
    template_folder="app/templates"
)

# Registro das rotas do blueprint
app.register_blueprint(core_bp)

if __name__ == "__main__":
    app.run(debug=True)
