from flask import Blueprint
from .UsuarioRoutes import usuario_bp
from .DenunciaRoutes import denuncia_bp
from .ReclamoRoutes import reclamo_bp
from .ServicioRoutes import servicio_bp



# Import the routes
def register_blueprints(app):
    
    app.register_blueprint(usuario_bp, url_prefix="/usuario")
    app.register_blueprint(denuncia_bp, url_prefix="/denuncia")
    app.register_blueprint(reclamo_bp, url_prefix="/reclamo")
    app.register_blueprint(servicio_bp, url_prefix="/servicio")
