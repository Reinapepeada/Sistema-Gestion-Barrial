class Config:
    DEBUG = True
    SECRET_KEY = 'tu_clave_secreta'
    # defino la URI de la base de datos
    # con driver de SQL Server mssql+pymssql://scott:tiger@hostname:port/dbname
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://alejandro:ale123.@localhost:1433/Municipio'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024