from app import db
from app.models.models import Reclamo

class ReclamoService:
    @staticmethod
    def get_all_reclamos():
        reclamos = db.session.execute(db.select(Reclamo).order_by(Reclamo.idReclamo)).scalars()
        return reclamos
    
    @staticmethod
    def get_reclamo_by_id(id):
        reclamo = db.session.execute(db.select(Reclamo).filter_by(idReclamo=id)).scalar()
        return reclamo
    
    @staticmethod
    def create_reclamo(data):
        new_reclamo = Reclamo(
            documento=data['documento'],
            idSitio=data['idSitio'],
            idDesperfecto=data['idDesperfecto'],
            descripcion=data['descripcion'],
            estado=data['estado'],
            idReclamoUnificado=data['idReclamoUnificado'],
            legajo=data['legajo']
        )
        db.session.add(new_reclamo)
        db.session.commit()
        return new_reclamo
    
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