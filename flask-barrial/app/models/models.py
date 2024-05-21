from app import db

class Desperfecto(db.Model):
    __tablename__ = 'desperfectos'
    idDesperfecto = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    idRubro = db.Column(db.Integer, db.ForeignKey('rubros.idRubro'), nullable=False)
    
class Rubro(db.Model):
    __tablename__ = 'rubros'
    idRubro = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    desperfectos = db.relationship('Desperfecto', backref='rubro', lazy=True)

class Barrio(db.Model):
    __tablename__ = 'barrios'
    idBarrio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    vecinos = db.relationship('Vecino', backref='barrio', lazy=True)

class Vecino(db.Model):
    __tablename__ = 'vecinos'
    documento = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String, nullable=False)
    codigoBarrio = db.Column(db.Integer, db.ForeignKey('barrios.idBarrio'), nullable=False)
    denuncias = db.relationship('Denuncia', backref='vecino', lazy=True)
    reclamos = db.relationship('Reclamo', backref='vecino', lazy=True)

class Denuncia(db.Model):
    __tablename__ = 'denuncias'
    idDenuncias = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String, db.ForeignKey('vecinos.documento'), nullable=False)
    idSitio = db.Column(db.Integer, db.ForeignKey('sitios.idSitio'), nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    aceptaResponsabilidad = db.Column(db.Boolean, nullable=False)

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
    denuncias = db.relationship('Denuncia', backref='sitio', lazy=True)
    reclamos = db.relationship('Reclamo', backref='sitio', lazy=True)

class Reclamo(db.Model):
    __tablename__ = 'reclamos'
    idReclamo = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String, db.ForeignKey('vecinos.documento'), nullable=False)
    idSitio = db.Column(db.Integer, db.ForeignKey('sitios.idSitio'), nullable=False)
    idDesperfecto = db.Column(db.Integer, db.ForeignKey('desperfectos.idDesperfecto'), nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    idReclamoUnificado = db.Column(db.Integer, nullable=True)
    legajo = db.Column(db.Integer, db.ForeignKey('personal.legajo'), nullable=False)
    movimientos = db.relationship('MovimientoReclamo', backref='reclamo', lazy=True)

class MovimientoReclamo(db.Model):
    __tablename__ = 'movimientosReclamo'
    idMovimiento = db.Column(db.Integer, primary_key=True)
    idReclamo = db.Column(db.Integer, db.ForeignKey('reclamos.idReclamo'), nullable=False)
    responsable = db.Column(db.String, nullable=False)
    causa = db.Column(db.String, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

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
    reclamos = db.relationship('Reclamo', backref='personal', lazy=True)