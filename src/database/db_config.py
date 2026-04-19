from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Asegúrate de poner aquí tu contraseña de MySQL de Toluca
DATABASE_URL = "mysql+pymysql://root:sandra64@localhost/lupitasoft_db"

# Configuramos el motor con un pool de conexiones estable
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# scoped_session es el secreto para que no se trabe el sistema
session_factory = sessionmaker(bind=engine)
SessionLocal = scoped_session(session_factory)

Base = declarative_base()

print("Hola")
