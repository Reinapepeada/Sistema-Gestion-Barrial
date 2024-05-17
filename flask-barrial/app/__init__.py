from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import item_bp
    app.register_blueprint(item_bp, url_prefix='/api/items')

    return app