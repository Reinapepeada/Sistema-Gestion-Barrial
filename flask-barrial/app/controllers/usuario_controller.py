from app.services.usuario_service import Usuario_service

class UsuarioController:
    @staticmethod
    def get_all_usuarios():
        return usuario_service.get_all_usuarios()
    
    @staticmethod
    def get_usuario_by_documento(documento):
        usuario_found = usuario_service.get_usuario_by_documento(documento)
        if usuario_found:
            return usuario_found, 200
        
        return "no se ha encontrado un usuario que corresponda", 404
    
    @staticmethod
    def first_login(data):
        try:
            usuario = Usuario_service.first_login(data)
            return usuario, 200
        except Exception as e:
            return str(e), 500
        
    @staticmethod
    def login(data):
        try:
            usuario = Usuario_service.login(data)
            if usuario:
                return usuario, 200
            return "usuario no encontrado", 404
        except Exception as e:
            return str(e), 404
        
    @staticmethod
    def forgot_password(data):
        try:
            usuario = Usuario_service.forgot_password(data)
            return usuario, 200
        except Exception as e:
            return str(e), 500
    
