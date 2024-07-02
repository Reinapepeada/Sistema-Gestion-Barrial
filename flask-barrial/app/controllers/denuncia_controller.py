
from flask import jsonify
from app.services.denuncia_service import DenunciaService

class DenunciaController:
    @staticmethod
    def get_all_denuncias():
        return DenunciaService.get_all_denuncias()
    
    @staticmethod
    def get_denuncia_by_id(id):
        denuncia_found = DenunciaService.get_denuncia_by_id(id)
        if denuncia_found:
            return denuncia_found, 200
        
        return "no se ha encontrado una denuncia que corresponda", 404
    
    @staticmethod
    def create_denuncia():
        new_denuncia = DenunciaService.create_denuncia()
        if new_denuncia:
            return new_denuncia, 201
        
        return "no se ha podido crear la denuncia", 400
    
    @staticmethod
    def update_denuncia(id, data):
        updated_denuncia = DenunciaService.update_denuncia(id, data)
        if updated_denuncia:
            return updated_denuncia, 200
        
        return "no se ha podido actualizar la denuncia", 404
    
    @staticmethod
    def delete_denuncia(id):
        deleted_denuncia = DenunciaService.delete_denuncia(id)
        if deleted_denuncia:
            return deleted_denuncia, 200
        
        return "no se ha podido eliminar la denuncia", 404
    
    @staticmethod
    def get_denuncias_by_vecino(documento):
        print("Denuncias:", "llego aca")
        try:
            denuncias = DenunciaService.get_denuncias_by_vecino(documento)
            if denuncias:
                return jsonify([denuncia.to_dict() for denuncia in denuncias]), 200
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": "An error occurred while fetching the denuncias"}), 500
    
    @staticmethod
    def get_denuncias_by_denunciado(documento):
        try:
            denuncias = DenunciaService.get_denuncias_by_denunciado(documento)
            if denuncias:
                return jsonify([denuncia.to_dict() for denuncia in denuncias]), 200
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": "An error occurred while fetching the denuncias"}), 500
        

    @staticmethod
    def get_denuncias_by_sitio(id):
        denuncias = DenunciaService.get_denuncias_by_sitio(id)
        if denuncias:
            return denuncias, 200
        
        return "no se han encontrado denuncias para el sitio", 404
    # Path: flask-barrial/app/services/denuncia_service.py