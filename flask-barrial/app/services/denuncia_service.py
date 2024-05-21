from app import db
from app.models.models import Denuncia



class DenunciaService:
    @staticmethod
    def get_all_denuncias():
        denuncias = db.session.execute(db.select(Denuncia).order_by(Denuncia.idDenuncias)).scalars()
        return denuncias
    
    @staticmethod
    def get_denuncia_by_id(id):
        denuncia = db.session.execute.select(Denuncia).filter_by(idDenuncias=id).scalar()
        return denuncia
    
    @staticmethod
    def create_denuncia(data):
        new_denuncia = Denuncia(
            documento=data['documento'],
            idSitio=data['idSitio'],
            descripcion=data['descripcion'],
            estado=data['estado'],
            aceptaResponsabilidad=data['aceptaResponsabilidad']
        )
        db.add(new_denuncia)
        db.commit()
        return new_denuncia
    
    @staticmethod
    def update_denuncia(id, data):
        updated_denuncia = db.session.execute.select(Denuncia).filter_by(idDenuncias=id).scalar()
        if updated_denuncia:
            updated_denuncia.documento = data['documento']
            updated_denuncia.idSitio = data['idSitio']
            updated_denuncia.descripcion = data['descripcion']
            updated_denuncia.estado = data['estado']
            updated_denuncia.aceptaResponsabilidad = data['aceptaResponsabilidad']
            db.commit()
        return updated_denuncia
    
    @staticmethod
    def delete_denuncia(id):
        deleted_denuncia = db.session.execute.select(Denuncia).filter_by(idDenuncias=id).scalar()
        if deleted_denuncia:
            db.delete(deleted_denuncia)
            db.commit()
        return deleted_denuncia
    
    @staticmethod
    def get_denuncias_by_vecino(documento):
        denuncias = db.session.execute.select(Denuncia).filter_by(documento=documento).scalars()
        return denuncias
    
    @staticmethod
    def get_denuncias_by_sitio(id):
        denuncias = db.session.execute.select(Denuncia).filter_by(idSitio=id).scalars()
        return denuncias