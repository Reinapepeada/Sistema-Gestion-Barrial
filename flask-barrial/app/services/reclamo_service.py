from flask import jsonify, request
from app import db
from app.models.models import Reclamo, Sitio, Desperfecto, FotosReclamos,Vecino,Personal
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
                sitio = db.session.execute(db.select(Sitio).filter_by(idSitio=reclamo.idSitio)).scalar()
                desperfecto = db.session.execute(db.select(Desperfecto).filter_by(idDesperfecto=reclamo.idDesperfecto)).scalar()
                fotosArray = []
                for foto in fotos:
                    fotosArray.append(foto.ruta)
                reclamos.append({
                    'idReclamo': reclamo.idReclamo,
                    'documento': reclamo.documento,
                    'sitio': sitio.descripcion if sitio else 'N/A',
                    'desperfecto': desperfecto.descripcion if desperfecto else 'N/A',
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
    
    def get_reclamos_by_user(documento):
        reclamos=[]
        reclamosSelect = db.session.execute(db.select(Reclamo).filter_by(documento=documento)).scalars()
        if reclamosSelect:
            for reclamo in reclamosSelect:
                sitio=db.session.execute(db.select(Sitio).filter_by(idSitio=reclamo.idSitio)).scalar()
                desperfecto=db.session.execute(db.select(Desperfecto).filter_by(idDesperfecto=reclamo.idDesperfecto)).scalar()
                # intenta traer al usuario de vecinos
                usuario = db.session.execute(db.select(Vecino).filter_by(documento=reclamo.documento)).scalar()
                if usuario is None:
                    # si no lo encuentra, intenta traer al usuario de personal
                    usuario = db.session.execute(db.select(Personal).filter_by(legajo=reclamo.documento)).scalar()
                fotos = db.session.execute(db.select(FotosReclamos).filter_by(reclamoid=reclamo.idReclamo)).scalars().all()
                fotosArray = []
                for foto in fotos:
                    fotosArray.append(foto.ruta)
                reclamos.append({
                    'idReclamo': reclamo.idReclamo,
                    'documento': reclamo.documento,
                    'usuario': usuario.to_dict() if usuario else None,
                    'idSitio': reclamo.idSitio,
                    'sitio': sitio.descripcion,
                    'idDesperfecto': reclamo.idDesperfecto,
                    'desperfecto': desperfecto.descripcion,
                    'descripcion': reclamo.descripcion,
                    'estado': reclamo.estado,
                    'idReclamoUnificado': reclamo.idReclamoUnificado,
                    'fotos': fotosArray
                })
        return jsonify(reclamos)
    
    
    @staticmethod
    def get_all_sitios():
        sitios = db.session.execute(db.select(Sitio)).scalars()
        if sitios:
            return sitios
        raise Exception("No se han encontrado sitios")
    
    @staticmethod
    def get_sitios_by_inspector(legajo):
        if not db.session.execute(db.select(Personal).filter_by(legajo=legajo)).scalar():
            raise Exception("No se ha encontrado el inspector")
        inspector = db.session.execute(db.select(Personal).filter_by(legajo=legajo)).scalar()
        sector = inspector.sector
        sitios = db.session.execute(db.select(Sitio)).scalars().all()

        # remover los sitios que no estan a cargo del inspector
        sitios = [sitio for sitio in sitios if sitio.aCargoDe in sector]
        sitios_dict = []
        for sitio in sitios:
                sitios_dict.append({
                    "idSitio": sitio.idSitio,
                    "descripcion": sitio.descripcion,
                })
        print("Sitios:", sitios)
        return jsonify(sitios_dict)
    
    @staticmethod
    def get_all_desperfectos():
        desperfectos = db.session.execute(db.select(Desperfecto)).scalars()
        if desperfectos:
            return desperfectos
        raise Exception("No se han encontrado desperfectos")
    
    @staticmethod
    def get_reclamos_by_inspector(documento):
        if not db.session.execute(db.select(Personal).filter_by(legajo=documento)).scalar():
            raise Exception("No se ha encontrado el inspector")
        # buscar inspector por legajo
        inspector = db.session.execute(db.select(Personal).filter_by(legajo=documento)).scalar()
        # alamcenar el sector del inspector
        sector = inspector.sector
        print("Sector:", sector)
        # traer todos los sitios 
        sitios = db.session.execute(db.select(Sitio)).scalars().all()
        # por cada sitio, ver si su sector esta dentro del sector del inspector(tiene espacios de mas el sector del inspector)
        sitios = [sitio for sitio in sitios if sitio.aCargoDe in sector]
        print("Sitios:", sitios)
        # buscar reclamos que tenga el sitio en el que el inspector esta a cargo
        reclamos = []
        for sitio in sitios:
            reclamos.extend(db.session.execute(db.select(Reclamo).filter_by(idSitio=sitio.idSitio)).scalars().all())
        print("Reclamos:", reclamos)
        # meter array de fotos en cada reclamo
        reclamos_dict = []
        for reclamo in reclamos:
            fotos = db.session.execute(db.select(FotosReclamos).filter_by(reclamoid=reclamo.idReclamo)).scalars().all()
            fotosArray = []
            for foto in fotos:
                fotosArray.append(foto.ruta)
            
            # buscar sitio
            sitio=db.session.execute(db.select(Sitio).filter_by(idSitio=reclamo.idSitio)).scalar()
            desperfecto=db.session.execute(db.select(Desperfecto).filter_by(idDesperfecto=reclamo.idDesperfecto)).scalar()
            # intenta traer al usuario de vecinos
            usuario = db.session.execute(db.select(Vecino).filter_by(documento=reclamo.documento)).scalar()
            if usuario is None:
                # si no lo encuentra, intenta traer al usuario de personal
                usuario = db.session.execute(db.select(Personal).filter_by(legajo=reclamo.documento)).scalar()
            
            reclamos_dict.append({
                    'idReclamo': reclamo.idReclamo,
                    'documento': reclamo.documento,
                    'usuario': usuario.to_dict() if usuario else None,
                    'idSitio': reclamo.idSitio,
                    'sitio': sitio.descripcion,
                    'idDesperfecto': reclamo.idDesperfecto,
                    'desperfecto': desperfecto.descripcion,
                    'descripcion': reclamo.descripcion,
                    'estado': reclamo.estado,
                    'idReclamoUnificado': reclamo.idReclamoUnificado,
                    'fotos': fotosArray
            })




        return jsonify(reclamos_dict)



