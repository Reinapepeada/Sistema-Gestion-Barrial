from flask import jsonify
from app.services.reclamo_service import ReclamoService

class ReclamoController:
    @staticmethod
    def get_all_reclamos():
        return ReclamoService.get_all_reclamos()
    
    @staticmethod
    def get_reclamo_by_id(id):
        reclamo_found = ReclamoService.get_reclamo_by_id(id)
        if reclamo_found:
            return reclamo_found, 200
        
        return "no se ha encontrado un reclamo que corresponda", 404
    
    @staticmethod
    def create_reclamo(data):
        new_reclamo = ReclamoService.create_reclamo(data)
        if new_reclamo:
            return jsonify({
                'success': True,
                'reclamo_id': new_reclamo.id
            }), 201
        
        return jsonify({"message": "No se ha podido crear el reclamo"}), 400
    
    @staticmethod
    def update_reclamo(id, data):
        updated_reclamo = ReclamoService.update_reclamo(id, data)
        if updated_reclamo:
            return updated_reclamo, 200
        
        return "no se ha podido actualizar el reclamo", 404
    
    @staticmethod
    def delete_reclamo(id):
        deleted_reclamo = ReclamoService.delete_reclamo(id)
        if deleted_reclamo:
            return deleted_reclamo, 200
        
        return "no se ha podido eliminar el reclamo", 404
    
    @staticmethod
    def get_reclamos_by_vecino(documento):
        reclamos = ReclamoService.get_reclamos_by_vecino(documento)
        if reclamos:
            return reclamos, 200
        
        return "no se han encontrado reclamos para el vecino", 404
    
    @staticmethod
    def get_reclamos_by_sitio(id):
        reclamos = ReclamoService.get_reclamos_by_sitio(id)
        if reclamos:
            return reclamos, 200
        
        return "no se han encontrado reclamos para el sitio", 404
    
    @staticmethod
    def get_all_sitios():
        try:
            sitiosAll = ReclamoService.get_all_sitios()
            sitios = []
            for sitio in sitiosAll:
                sitios.append({
                    "idSitio": sitio.idSitio,
                    "descripcion": sitio.descripcion,
                })
            
            return sitios, 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def get_all_desperfectos():
        try:
            desperfectosAll = ReclamoService.get_all_desperfectos()
            desperfectos = []
            for desperfecto in desperfectosAll:
                desperfectos.append(desperfecto.to_dict())
            
            return desperfectos, 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500