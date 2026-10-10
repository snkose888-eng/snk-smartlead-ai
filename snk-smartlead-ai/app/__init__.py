import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import DevelopmentConfig, ProductionConfig
from .database import init_db
from .routes import bp

def create_app():
    app = Flask(__name__)
    config = ProductionConfig if os.environ.get("FLASK_ENV") == "production" else DevelopmentConfig
    app.config.from_object(config)

    origins = app.config.get("CORS_ORIGINS", "*")
    CORS(app)

    init_db(app)
    app.register_blueprint(bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "SNK SmartLead AI"}), 200

    return app
