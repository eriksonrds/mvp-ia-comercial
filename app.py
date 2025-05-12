from flask import Flask
from app.core.routes import core_bp  # Blueprint principal

app = Flask(
    __name__,
    static_folder="app/static",
    template_folder="app/templates"
)

app.register_blueprint(core_bp)

if __name__ == "__main__":
    app.run(debug=True)
