from flask import jsonify, request
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
            # revisa si hay foto
            
            # if 'files' not in data.files:
            #     return jsonify({"error": "No files part in the request"}), 400

            # # revisa si hay mas de 7 fotos 
            # files = data.getlist('files')
            # print(files)
            # if len(files) > 7:
            #     return jsonify({"error": "No more than 7 files allowed"}), 400

            # si cumple con todo eso que vaya al servicio 
            return ServicioService.create_servicio(data), 201
        
        except Exception as e:
            return str(e), 500