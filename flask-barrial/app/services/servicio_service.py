from flask import app, json, jsonify, request
from app import db
from app.models.models import Servicio, Foto
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

# funcion para saber si el archivo es permitido
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ServicioService:
    @staticmethod
    def get_all_servicios():
        serviciosArray = []
        servicios = db.session.execute(db.select(Servicio).order_by(Servicio.id)).scalars().all()

        if servicios:
            for servicio in servicios:
                fotosArray = []
                for foto in servicio.fotos:
                    fotosArray.append(foto.ruta)
                
                serviciosArray.append({
                    'id': servicio.id,
                    'idVecino': servicio.idVecino,
                    'titulo': servicio.titulo,
                    'descripcion': servicio.descripcion,
                    'numeroCelular': servicio.numeroCelular,
                    'idEstado': servicio.idEstado,
                    'oferta': servicio.oferta,
                    'fotos': fotosArray
                })

        return jsonify(serviciosArray)
        
    @staticmethod
    def get_servicios_by_user(id):
        serviciosArray = []
        #  traer los servicios de un vecino
        servicios = db.session.execute(db.select(Servicio).filter_by(idVecino=id)).scalars().all()
        if servicios:
            for servicio in servicios:
                fotosArray = []
                for foto in servicio.fotos:
                    fotosArray.append(foto.ruta)
                
                serviciosArray.append({
                    'id': servicio.id,
                    'idVecino': servicio.idVecino,
                    'titulo': servicio.titulo,
                    'descripcion': servicio.descripcion,
                    'numeroCelular': servicio.numeroCelular,
                    'idEstado': servicio.idEstado,
                    'oferta': servicio.oferta,
                    'fotos': fotosArray
                })

        return jsonify(serviciosArray)
    
    @staticmethod
    def create_servicio(data):
        try:
            # Extract form data
            data = request.form
            print("Received data:", data)

            # Extract files from the request
            files = request.files.getlist("files")
            print("Received files:", files)

            # Create new servicio
            new_servicio = Servicio(
                idVecino=data['documento'],
                titulo=data['titulo'],
                descripcion=data['descripcion'],
                oferta=data['oferta'],
                numeroCelular=data['numeroCelular'],
                idEstado=1
            )

            # Generate current date and time
            current_date = datetime.now().date()
            current_time = datetime.now().time()

            # Set the date and time for the new servicio
            new_servicio.fecha = current_date
            new_servicio.hora = current_time

            db.session.add(new_servicio)
            db.session.commit()

            # Save photos and associate them with the servicio
            for file in files:
                print("File:", file)
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    file_path = os.path.join(os.getcwd(), '/app/uploads', unique_filename)
                    file.save(file_path)
                    ruta_relativa = f"uploads/{unique_filename}"
                    foto = Foto(servicio_id=new_servicio.id, ruta=ruta_relativa)
                    db.session.add(foto)
                else:
                    db.session.rollback()
                    return jsonify({"error": f"File {file.filename} is not allowed"}), 400

            db.session.commit()
            return new_servicio.to_dict()

        except Exception as e:
            db.session.rollback()
            print("Error in create_servicio:", e)
            return jsonify({"error": str(e)}), 500

        
    
    @staticmethod
    def delete_servicio(id):
        try:
            servicio = db.session.execute(db.select(Servicio).filter_by(id=id)).scalar_one()
            # elimino las fotos asociadas al servicio
            fotos = db.session.execute(db.select(Foto).filter_by(servicio_id=id)).scalars().all()
            # si hay fotos las elimino
            if fotos:
                for foto in fotos:
                    db.session.delete(foto)
            # elimino el servicio
            db.session.delete(servicio)
            db.session.commit()
            return jsonify({"message": "Servicio deleted successfully"})
        except Exception as e:
            db.session.rollback()
            print("Error in delete_servicio:", e)
            return jsonify({"error": str(e)})