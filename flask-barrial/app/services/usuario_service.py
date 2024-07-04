from app import db
from app.models.models import Vecino,Personal
from werkzeug.security import generate_password_hash, check_password_hash

# librerias para enviar correos y generar contraseñas temporales
import smtplib
import string
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_temporary_password(length=8):
    # Generate a temporary password with a default length of 8
    # The password will be a mix of uppercase, lowercase and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_email(receiver_email, subject, message):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to the email account
    sender_email = 'teamcelular.arg@gmail.com'
    sender_password = 'fspf didi hwen rhjq'
    server.login(sender_email, sender_password)

    # Create the email
    email = MIMEMultipart()
    email['From'] = sender_email
    email['To'] = receiver_email
    email['Subject'] = subject
    email.attach(MIMEText(message, 'plain'))

    # Send the email
    server.send_message(email)
    server.quit()

class Usuario_service:
    @staticmethod
    def get_all_usuarios():
        vecinos = db.session.execute(db.select(Vecino).order_by(Vecino.codigoBarrio)).scalars()
        return vecinos
    
    @staticmethod
    def get_usuario_by_id(documento):
        # se fija si existe en vecino
        vecino = db.session.execute(db.select(Vecino).filter_by(documento=documento)).scalar()
        
        if vecino :
            vecinojson = {
                "documento": vecino.documento,
                "nombre": vecino.nombre,
                "apellido": vecino.apellido,
                "direccion": vecino.direccion,
                "email": vecino.email,
                "codigoBarrio": vecino.codigoBarrio,
                "tipo": "vecino"
            }
            return vecinojson
        # se fija si existe en personal
        personal = db.session.execute(db.select(Personal).filter_by(legajo=documento)).scalar()
        if personal:
            personaljson = {
                "documento": personal.legajo,
                "nombre": personal.nombre,
                "apellido": personal.apellido,
                "direccion": personal.direccion,
                "codigoBarrio": personal.codigoBarrio,
                "email": personal.email,
                "tipo": "personal"
            }
            return personaljson
        return None
    
    @staticmethod
    def first_login(data):
        # agregamos el prefijo "DNI" al documento
        data['documento'] = 'DNI' + data['documento']

        # Primero verificamos en la tabla de Personal
        vecino = db.session.execute(db.select(Vecino).filter_by(documento=data['documento'])).scalar()
        if vecino and vecino.documento == data['documento']:
            temporary_password = generate_temporary_password()
            message = f"Your temporary password is: {temporary_password}"
            send_email(data['email'], "clave temporal", message)
            # cifrar la contraseña temporal
            hashed_password = generate_password_hash(temporary_password)
            # actualizar la contraseña temporal en la base de datos
            print(hashed_password)
            vecino.password = hashed_password
            vecino.email = data['email']
            db.session.commit()
            # convirtiendo el objeto vecino a un json
            vecino_json = vecino.to_dict()
        return vecino_json    
    
    @staticmethod
    def login(data):
        # Primero verificamos en la tabla de Personal
        personal = db.session.execute(db.select(Personal).filter_by(legajo=data['documento'])).scalar()
        if personal and personal.password == data['password']:
            return {
                'user_type': 'inspector',
                'user_data': personal.to_dict()
            }


        # agregamos el prefijo "DNI" al documento porque asi esta en la base de datos
        data['documento'] = 'DNI' + data['documento']
        # Si no está en Personal, verificamos en la tabla de Vecino
        vecino = db.session.execute(db.select(Vecino).filter_by(documento=data['documento'])).scalar()
        if vecino and check_password_hash(vecino.password, data['password']):
            return {
                'user_type': 'vecino',
                'user_data': vecino.to_dict()
            }

        raise ValueError("El email o la contraseña no corresponden a un usuario en el sistema")

    @staticmethod
    def forgot_password(data):
        data['documento'] = 'DNI' + data['documento']
        vecino = db.session.execute(db.select(Vecino).filter_by(documento=data['documento'])).scalar()
        if vecino:
            temporary_password = generate_temporary_password()
            message = f"Your temporary password is: {temporary_password}"
            send_email(vecino.email, "clave temporal", message)
            # cifrar la contraseña temporal
            hashed_password = generate_password_hash(temporary_password)
            # actualizar la contraseña temporal en la base de datos
            vecino.password = hashed_password
            db.session.commit()
            return vecino.to_dict()
        raise ValueError("El documento no corresponde a un usuario en el sistema")
    
    @staticmethod
    def change_password(data):
        print(data)
        vecino = db.session.execute(db.select(Vecino).filter_by(documento=data['documento'])).scalar()
        if vecino and check_password_hash(vecino.password, data['currentPassword']):
            hashed_password = generate_password_hash(data['newPassword'])
            vecino.password = hashed_password
            db.session.commit()
            return vecino.to_dict()
        raise ValueError("El documento o la contraseña actual no corresponden a un usuario en el sistema")
    