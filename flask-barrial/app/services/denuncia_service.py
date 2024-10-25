import datetime
from flask import jsonify, request
from app import db
from app.models.models import Denuncia, FotosDenuncias

from werkzeug.utils import secure_filename
import os
import uuid


# funcion para saber si el archivo es permitido
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
    }
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class DenunciaService:
    @staticmethod
    def get_all_denuncias():

        denuncias = db.session.execute(
            db.select(Denuncia).order_by(Denuncia.idDenuncias)
        ).scalars()
        return denuncias

    @staticmethod
    def get_denuncias_by_vecino(documento):
        print("Denuncias:", "llego aca")
        denuncias=[]
        denunciasSelect = db.session.execute(
            db.select(Denuncia).filter_by(documento=documento)
        ).scalars()


        for denuncia in denunciasSelect:

            fotos = db.session.execute(db.select(FotosDenuncias).filter_by(denunciaId=denuncia.idDenuncias)).scalars().all()
            fotosArray = []
            for foto in fotos:
                fotosArray.append(foto.ruta)
            
            date=denuncia.horayFecha
            date=date.strftime("%d/%m/%Y %H:%M:%S")
            denuncias.append({
                "idDenuncias": denuncia.idDenuncias,
                "comercio": denuncia.comercio,
                "tipoDenuncia": denuncia.tipoDenuncia,
                "descripcion": denuncia.descripcion,
                "estado": denuncia.estado,
                "aceptaResponsabilidad": denuncia.aceptaResponsabilidad,
                "ubicacion": denuncia.ubicacion,
                "horayFecha": date,
                "denunciadoDocumento": denuncia.denunciadoDocumento,
                "documento": denuncia.documento,
                "fotos": fotosArray
            })
        return jsonify(denuncias)
            



    @staticmethod
    def get_denuncias_by_denunciado(documento):
        denuncias=[]
        denunciasSelect = db.session.execute(
            db.select(Denuncia).filter_by(denunciadoDocumento=documento)
        ).scalars()
        for denuncia in denunciasSelect:
            date=denuncia.horayFecha
            date=date.strftime("%d/%m/%Y %H:%M:%S")

            fotos = db.session.execute(db.select(FotosDenuncias).filter_by(denunciaId=denuncia.idDenuncias)).scalars().all()
            fotosArray = []
            for foto in fotos:
                fotosArray.append(foto.ruta)
            
            denuncias.append({
                "idDenuncias": denuncia.idDenuncias,
                "comercio": denuncia.comercio,
                "tipoDenuncia": denuncia.tipoDenuncia,
                "descripcion": denuncia.descripcion,
                "estado": denuncia.estado,
                "aceptaResponsabilidad": denuncia.aceptaResponsabilidad,
                "ubicacion": denuncia.ubicacion,
                "horayFecha": date,
                "denunciadoDocumento": denuncia.denunciadoDocumento,
                "documento": denuncia.documento,
                "fotos": fotosArray
                })
        return jsonify(denuncias)

    @staticmethod
    def get_denuncia_by_id(id):
        denuncia = (
            db.session.execute.select(Denuncia).filter_by(idDenuncias=id).scalar()
        )
        return denuncia

    @staticmethod
    def create_denuncia():
        try:
            data = request.form
            print("Received data:", data)

            files = request.files.getlist("files")
            print("Received files:", files)
            horaYFecha = datetime.datetime.now()
            documento = data.get("documento", None)

            if data["denunciaType"] == "comercio":
                denuncia = Denuncia(
                    comercio=data["comercio"],
                    tipoDenuncia=data["denunciaType"],
                    descripcion=data["descripcion"],
                    estado="pendiente",
                    aceptaResponsabilidad=False,
                    ubicacion=data["ubicacion"],
                    horayFecha=horaYFecha,
                    documento=documento
                )
            else:
                denuncia = Denuncia(
                    documento=documento,
                    tipoDenuncia=data["denunciaType"],
                    descripcion=data["descripcion"],
                    estado="pendiente",
                    denunciadoDocumento=data["denunciadoDocumento"],
                    aceptaResponsabilidad=False,
                    ubicacion=data["ubicacion"],
                    horayFecha=horaYFecha  # Asegúrate de que el nombre sea correcto
                )

            db.session.add(denuncia)
            db.session.commit()
            print("Denuncia creada con exito", denuncia)

                         # Ensure the upload directory exists
            upload_folder = os.path.join(os.getcwd(), 'app', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            for file in files:
                print("File:", file)
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    file_path = os.path.join(upload_folder, unique_filename)
                    file.save(file_path)
                    ruta_relativa = f"uploads/{unique_filename}"
                    foto = FotosDenuncias(
                        denunciaId=denuncia.idDenuncias, ruta=ruta_relativa
                    )
                    db.session.add(foto)
                else:
                    db.session.rollback()
                    return jsonify({"error": f"File {file.filename} is not allowed"}), 400

            db.session.commit()
            return jsonify(denuncia.to_dict())
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": "An error occurred while creating the denuncia"})

    @staticmethod
    def update_denuncia(id, data):
        updated_denuncia = (
            db.session.execute.select(Denuncia).filter_by(idDenuncias=id).scalar()
        )
        if updated_denuncia:
            updated_denuncia.documento = data["documento"]
            updated_denuncia.idSitio = data["idSitio"]
            updated_denuncia.descripcion = data["descripcion"]
            updated_denuncia.estado = data["estado"]
            updated_denuncia.aceptaResponsabilidad = data["aceptaResponsabilidad"]
            db.commit()
        return updated_denuncia

    @staticmethod
    def delete_denuncia(id):
        deleted_denuncia = (
            db.session.execute.select(Denuncia).filter_by(idDenuncias=id).scalar()
        )
        if deleted_denuncia:
            db.delete(deleted_denuncia)
            db.commit()
        return deleted_denuncia


