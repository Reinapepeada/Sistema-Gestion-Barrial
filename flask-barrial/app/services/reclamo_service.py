from flask import jsonify, request
from app import db
from app.models.models import Reclamo, Sitio, Desperfecto, FotosReclamos
from werkzeug.utils import secure_filename
import os
import uuid

# funcion para saber si el archivo es permitido
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class ReclamoService:
    @staticmethod
    def get_all_reclamos():
        reclamos = []
        reclamosSelect = db.session.execute(db.select(Reclamo).order_by(Reclamo.idReclamo)).scalars()
        if reclamosSelect:
            for reclamo in reclamosSelect:
                fotos = db.session.execute(db.select(FotosReclamos).filter_by(reclamoid=reclamo.idReclamo)).scalars().all()
                fotosArray = []
                for foto in fotos:
                    fotosArray.append(foto.ruta)
                reclamos.append({
                    'idReclamo': reclamo.idReclamo,
                    'documento': reclamo.documento,
                    'idSitio': reclamo.idSitio,
                    'idDesperfecto': reclamo.idDesperfecto,
                    'descripcion': reclamo.descripcion,
                    'estado': reclamo.estado,
                    'idReclamoUnificado': reclamo.idReclamoUnificado,
                    'fotos': fotosArray
                })
        return jsonify(reclamos)
    
    @staticmethod
    def get_reclamo_by_id(id):
        reclamo = db.session.execute(db.select(Reclamo).filter_by(idReclamo=id)).scalar()
        return reclamo
    

    @staticmethod
    def create_reclamo():
        try:
            data = request.form
            print("Received data:", data)

            files = request.files.getlist("files")
            print("Received files:", files)

            idReclamoUnificado = data.get('idReclamoUnificado', 0)

            # Validate idSitio
            sitio_exists = db.session.query(Sitio).filter_by(idSitio=data['sitio']).first()
            if not sitio_exists:
                print(f"Error: Sitio {data['sitio']} does not exist")
                return jsonify({"error": "The specified sitio does not exist."}), 400

            #  convertir a integer
            sitio = int(data['sitio'])
            #  convertir a integer
            desper = int(data['desperfecto'])

            new_reclamo = Reclamo(
                documento=data['documento'],
                idSitio=sitio,
                idDesperfecto=desper,
                descripcion=data['descripcion'],
                idReclamoUnificado=idReclamoUnificado,
            )
            db.session.add(new_reclamo)
            db.session.commit()
            print("New reclamo:", new_reclamo)

            # Save photos and associate them with the servicio
            for file in files:
                print("File:", file)
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    file_path = os.path.join(os.getcwd(), 'uploads', unique_filename)
                    file.save(file_path)
                    ruta_relativa = f"uploads/{unique_filename}"
                    foto = FotosReclamos(reclamoid=new_reclamo.idReclamo, ruta=ruta_relativa)
                    db.session.add(foto)
                else:
                    db.session.rollback()
                    return jsonify({"error": f"File {file.filename} is not allowed"}), 400

            db.session.commit()
            return jsonify(new_reclamo.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            print("Error in create_reclamo:", e)
            return jsonify({"error": str(e)}), 500
            
    
    @staticmethod
    def update_reclamo(id, data):
        updated_reclamo = db.session.execute(db.select(Reclamo).filter_by(idReclamo=id)).scalar()
        if updated_reclamo:
            updated_reclamo.documento = data['documento']
            updated_reclamo.idSitio = data['idSitio']
            updated_reclamo.idDesperfecto = data['idDesperfecto']
            updated_reclamo.descripcion = data['descripcion']
            updated_reclamo.estado = data['estado']
            updated_reclamo.idReclamoUnificado = data['idReclamoUnificado']
            updated_reclamo.legajo = data['legajo']
            db.session.commit()
        return updated_reclamo
    
    @staticmethod
    def delete_reclamo(id):
        deleted_reclamo = db.session.execute(db.select(Reclamo).filter_by(idReclamo=id)).scalar()
        if deleted_reclamo:
            db.session.delete(deleted_reclamo)
            db.session.commit()
        return deleted_reclamo
    
    @staticmethod
    def get_reclamos_by_vecino(documento):
        reclamos = db.session.execute(db.select(Reclamo).filter_by(documento=documento)).scalars()
        return reclamos
    
    @staticmethod
    def get_reclamos_by_sitio(id):
        reclamos = db.session.execute(db.select(Reclamo).filter_by(idSitio=id)).scalars()
        return reclamos
    
    @staticmethod
    def get_all_sitios():
        sitios = db.session.execute(db.select(Sitio)).scalars()
        if sitios:
            return sitios
        raise Exception("No se han encontrado sitios")
    
    @staticmethod
    def get_all_desperfectos():
        desperfectos = db.session.execute(db.select(Desperfecto)).scalars()
        if desperfectos:
            return desperfectos
        raise Exception("No se han encontrado desperfectos")
    # 
        
