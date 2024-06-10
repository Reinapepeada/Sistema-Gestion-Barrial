from app import db
from app.models.models import Vecino
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
        vecino = db.session.execute(db.select(Vecino).filter_by(documento=documento)).scalar()
        return vecino
    
    @staticmethod
    def first_login(data):
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
            db.session.commit()
            # convirtiendo el objeto vecino a un json
            vecino_json = vecino.to_dict()
        return vecino_json    
    
    @staticmethod
    def login(data):
        vecino = db.session.execute(db.select(Vecino).filter_by(documento=data['documento'])).scalar()
        if vecino and check_password_hash(vecino.password, data['password']):
            return vecino.to_dict()
        raise ValueError("El documento o la contraseña no corresponden a un usuario en el sistema")
