from app import db
from app.models.models import Servicio

class ServicioService:
    @staticmethod
    def get_all_servicios():
        servicios = db.session.execute(db.select(Servicio).order_by(Servicio.idServicio)).scalars()
        return servicios
    
    @staticmethod
    def get_servicios_by_user(id):
        servicios = db.session.execute(db.select(Servicio).filter_by(idVecino=id)).scalars()
        return servicios
    
    @staticmethod
    def create_servicio(data):
        new_servicio = Servicio(
            idVecino=data['idVecino'],
            idReclamo=data['idReclamo'],
            fecha=data['fecha'],
            hora=data['hora'],
            idEstado=data['idEstado']
        )
        db.session.add(new_servicio)
        db.session.commit()
        return new_servicio
    
    @staticmethod
    def update_servicio(id, data):
        updated_servicio = db.session.execute(db.select(Servicio).filter_by(idServicio=id)).scalar()
        if updated_servicio:
            updated_servicio.idVecino = data['idVecino']
            updated_servicio.idReclamo = data['idReclamo']
            updated_servicio.fecha = data['fecha']
            updated_servicio.hora = data['hora']
            updated_servicio.idEstado = data['idEstado']
            db.session.commit()
        return updated_servicio
    
    @staticmethod
    def delete_servicio(id):
        deleted_servicio = db.session.execute(db.select(Servicio).filter_by(idServicio=id)).scalar()
        if deleted_servicio:
            db.session.delete(deleted_servicio)
            db.session.commit()
        return deleted_servicio