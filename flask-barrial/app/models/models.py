from app import db

class Vecinos (db.Model):
    __tablename__ = 'vecinos'
    documento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    codigoBarrio = db.Column(db.Integer, db.ForeignKey('barrios.idBarrio'), nullable=False)