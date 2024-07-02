from app import db

class Desperfecto(db.Model):
    __tablename__ = 'desperfectos'
    idDesperfecto = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    
    def to_dict(self):
        return {
            'idDesperfecto': self.idDesperfecto,
            'descripcion': self.descripcion,
        }
    

class Foto(db.Model):
    __tablename__ = 'fotos'
    id = db.Column(db.Integer, primary_key=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)  # Updated ForeignKey
    ruta = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'servicio_id': self.servicio_id,
            'ruta': self.ruta
        }

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    idVecino = db.Column(db.Integer,db.ForeignKey('vecinos.documento'), nullable=False)
    titulo = db.Column(db.String, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    oferta = db.Column(db.String, nullable=True)
    numeroCelular = db.Column(db.String, nullable=True)
    descripcion = db.Column(db.String, nullable=False)
    idEstado = db.Column(db.Integer, nullable=False)
    fotos = db.relationship('Foto', backref='servicio', lazy=True)

    def to_dict(self):
        return {
            'idVecino': self.idVecino,
            'titulo': self.titulo,
            'oferta': self.oferta,
            'numeroCelular': self.numeroCelular,
            'descripcion': self.descripcion,
            'idEstado': self.idEstado
        }


class Barrio(db.Model):
    __tablename__ = 'barrios'
    idBarrio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    vecinos = db.relationship('Vecino', backref='barrio', lazy=True)
    
    def to_dict(self):
        return {
            'idBarrio': self.idBarrio,
            'nombre': self.nombre
        }

class Vecino(db.Model):
    __tablename__ = 'vecinos'
    documento = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String, nullable=False)
    codigoBarrio = db.Column(db.Integer, db.ForeignKey('barrios.idBarrio'), nullable=False)
    
    reclamos = db.relationship('Reclamo', backref='vecino', lazy=True)
    password = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    
    def to_dict(self):
        return {
            'documento': self.documento,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'direccion': self.direccion,
            'email': self.email
        }

class Denuncia(db.Model):
    __tablename__ = 'denuncias'
    idDenuncias = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String, db.ForeignKey('vecinos.documento'), nullable=False)
    denunciadoDocumento = db.Column(db.String,db.ForeignKey('vecinos.documento'), nullable=True )
    comercio = db.Column(db.String, nullable=True)
    tipoDenuncia = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    aceptaResponsabilidad = db.Column(db.Boolean, nullable=False)
    ubicacion=db.Column(db.String, nullable=False)
    horayFecha = db.Column(db.DateTime, nullable=True)
    def to_dict(self):
        return {
            'idDenuncias': self.idDenuncias,
            'documento': self.documento,
            'denunciadoDocumento': self.denunciadoDocumento,
            'comercio': self.comercio,
            'tipoDenuncia': self.tipoDenuncia,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'aceptaResponsabilidad': self.aceptaResponsabilidad,
            'ubicacion': self.ubicacion,
            'horayFecha': self.horayFecha
        }

class Sitio(db.Model):
    __tablename__ = 'sitios'
    idSitio = db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    calle = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    entreCalleA = db.Column(db.String, nullable=True)
    entreCalleB = db.Column(db.String, nullable=True)
    descripcion = db.Column(db.String, nullable=True)
    aCargoDe = db.Column(db.String, nullable=True)
    apertura = db.Column(db.Date, nullable=True)
    cierre = db.Column(db.Date, nullable=True)
    comentarios = db.Column(db.String, nullable=True)
    reclamos = db.relationship('Reclamo', backref='sitio', lazy=True)
    
    def to_dict(self):
        return {
            'idSitio': self.idSitio,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'calle': self.calle,
            'numero': self.numero,
            'entreCalleA': self.entreCalleA,
            'entreCalleB': self.entreCalleB,
            'descripcion': self.descripcion,
            'aCargoDe': self.aCargoDe,
            'apertura': self.apertura,
            'cierre': self.cierre,
            'comentarios': self.comentarios
        }

class Reclamo(db.Model):
    __tablename__ = 'reclamos'
    idReclamo = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String, db.ForeignKey('vecinos.documento'), nullable=False)
    idSitio = db.Column(db.Integer, db.ForeignKey('sitios.idSitio'), nullable=False)
    idDesperfecto = db.Column(db.Integer, db.ForeignKey('desperfectos.idDesperfecto'), nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    # estado por defecto es 'pendiente'
    estado = db.Column(db.String, nullable=False, default='pendiente')
    #  ide de reclamo unificado por defecto es 0 y cuando se quiere unificar se le asigna el id del reclamo al cual se unifica
    idReclamoUnificado = db.Column(db.Integer, nullable=False, default=0)
    movimientos = db.relationship('MovimientoReclamo', backref='reclamo', lazy=True)
    
    def to_dict(self):
        return {
            'idReclamo': self.idReclamo,
            'documento': self.documento,
            'idSitio': self.idSitio,
            'idDesperfecto': self.idDesperfecto,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'idReclamoUnificado': self.idReclamoUnificado,
        }

class MovimientoReclamo(db.Model):
    __tablename__ = 'movimientosReclamo'
    idMovimiento = db.Column(db.Integer, primary_key=True)
    idReclamo = db.Column(db.Integer, db.ForeignKey('reclamos.idReclamo'), nullable=False)
    responsable = db.Column(db.String, nullable=False)
    causa = db.Column(db.String, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'idMovimiento': self.idMovimiento,
            'idReclamo': self.idReclamo,
            'responsable': self.responsable,
            'causa': self.causa,
            'fecha': self.fecha
        }
    

class FotosReclamos(db.Model):
    __tablename__ = 'fotosReclamos'

    id = db.Column(db.Integer, primary_key=True)
    reclamoid = db.Column(db.Integer, db.ForeignKey('reclamos.idReclamo'), nullable=False)
    ruta = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'reclamoid': self.reclamoid,
            'ruta': self.ruta
        }
    
class FotosDenuncias(db.Model): 
    __tablename__ = 'fotosDenuncias'
    id = db.Column(db.Integer, primary_key=True)
    denunciaId = db.Column(db.Integer, db.ForeignKey('denuncias.idDenuncias'), nullable=False)
    ruta = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'denunciaid': self.denunciaId,
            'ruta': self.ruta
        }
    
class Personal(db.Model):
    __tablename__ = 'personal'
    legajo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    documento = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    sector = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String, nullable=False)
    fechaIngreso = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'legajo': self.legajo,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'sector': self.sector,
            'categoria': self.categoria,
            'fechaIngreso': self.fechaIngreso
        }