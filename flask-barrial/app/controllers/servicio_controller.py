from app.services.servicio_service import ServicioService

class ServicioController:
    @staticmethod
    def get_all_servicios():
        try:
            return ServicioService.get_all_servicios(), 200
        except Exception as e:
            return str(e), 500
    @staticmethod
    def get_servicios_by_user(idUser):
        try:
            return ServicioService.get_servicios_by_user(idUser), 200
        except Exception as e:
            return str(e), 500
        
    @staticmethod
    def create_servicio(data):
        try:
            return ServicioService.create_servicio(data), 201
        except Exception as e:
            return str(e), 500