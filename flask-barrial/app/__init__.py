# app/__init__.py

import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Crear la instancia de la base de datos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Configurar app
    app.config.from_object('app.config.Config')
    # Inicializar db
    db.init_app(app)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Registrar Blueprints
    from .routes import register_blueprints
    register_blueprints(app)

    # Crear ruta de bienvenida
    @app.route('/')
    def hello():
        return {"message": "¡Bienvenido a la API de Barrial! La mejor API para administrar tu barrio!"}

    return app