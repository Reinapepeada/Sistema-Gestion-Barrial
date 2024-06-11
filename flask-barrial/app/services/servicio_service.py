from flask import app, jsonify
from app import db
from app.models.models import Servicio, Foto
from werkzeug.utils import secure_filename
import os

# funcion para saber si el archivo es permitido
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ServicioService:
    @staticmethod
    def get_all_servicios():
        servicios = db.session.execute(db.select(Servicio).order_by(Servicio.idServicio)).scalars()
        return jsonify([servicio.to_dict() for servicio in servicios])
    
    @staticmethod
    def get_servicios_by_user(id):
        servicios = db.session.execute(db.select(Servicio).filter_by(idVecino=id)).scalars()
        return jsonify([servicio.to_dict() for servicio in servicios])
    
    @staticmethod
    def create_servicio(data):
        
        files = data.getlist('files')

        # ejemplo de como se ve el data
        # {
        #   "idVecino": "123",
        #   "idReclamo": "456",
        #   "fecha": "2024-06-10",
        #   "hora": "14:30",
        #   "idEstado": "1",
        #   "files": [
        #     {
        #       "name": "photo1.jpg",
        #       "type": "image/jpeg",
        #       "uri": "file:///path/to/photo1.jpg"
        #     },
        #     {
        #       "name": "photo2.png",
        #       "type": "image/png",
        #       "uri": "file:///path/to/photo2.png"
        #     }
        #   ]
        # }   

        # Crear nuevo servicio
        new_servicio = Servicio(
            idVecino=data['idVecino'],
            titulo=data['titulo'],
            descripcion=data['descripcion'],
            fecha=data['fecha'],
            hora=data['hora'],
            idEstado=data['idEstado']
        )
        db.session.add(new_servicio)
        db.session.commit()

        # Guardar fotos y asociarlas al servicio
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                foto = Foto(servicio_id=new_servicio.id, ruta=file_path)
                db.session.add(foto)
            else:
                db.session.rollback()
                return jsonify({"error": f"File {file.filename} is not allowed"}), 400
        
        db.session.commit()
        return jsonify(new_servicio.to_dict())
    
    @staticmethod
    def update_servicio(id, data):
        servicio = db.session.execute(db.select(Servicio).filter_by(idServicio=id)).scalar()
        if not servicio:
            return jsonify({"error": "Servicio not found"}), 404
        
        servicio.descripcion = data['descripcion']
        servicio.fecha = data['fecha']
        servicio.hora = data['hora']
        # update fotos
        files = data.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                foto = Foto(servicio_id=servicio.id, ruta=file_path)
                db.session.add(foto)
            else:
                db.session.rollback()
                return jsonify({"error": f"File {file.filename} is not allowed"}), 400
        
        # busca y eliminar las fotos que no estan en la lista de files y en la carpeta
        fotos = db.session.execute(db.select(Foto).filter_by(servicio_id=id)).scalars()
        for foto in fotos:
            try:
                if foto.ruta not in [file.filename for file in files]:
                    os.remove(foto.ruta)
                    db.session.delete(foto)
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": f"Failed to delete photo: {str(e)}"}), 500
        
        # envio todos los datos en a la base de datos  
        db.session.commit()

        return jsonify(servicio.to_dict())
