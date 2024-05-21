from flask import Blueprint
from .usuarios import usuarios_bp
from .denuncia import denuncias_bp
from .reclamo import reclamos_bp
from .servicio import servicios_bp



# Import the routes
def register_blueprints(app):
    
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(denuncias_bp, url_prefix="/denuncias")
    app.register_blueprint(reclamos_bp, url_prefix="/reclamos")
    app.register_blueprint(servicios_bp, url_prefix="/servicios")
