import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy



# creo la instancia de la base de datos
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
        return send_from_directory('uploads', filename)


    # Registrar Blueprints
    from .routes import register_blueprints
    register_blueprints(app)

    # crear ruta de bienvenida
    @app.route('/')
    def hello():
        return {"message": "welcome to barrial api!  La mejor api para administrar tu Barrio!"}

    return app