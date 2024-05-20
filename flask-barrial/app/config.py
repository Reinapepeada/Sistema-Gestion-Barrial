class Config:
    DEBUG = True
    SECRET_KEY = 'tu_clave_secreta'
    # defino la URI de la base de datos
    # con driver de SQL Server mssql+pymssql://scott:tiger@hostname:port/dbname
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://holahola:holahola123.@localhost:1433/Municipio'