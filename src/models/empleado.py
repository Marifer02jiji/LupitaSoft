from sqlalchemy import Column, Integer, String
from src.database.db_config import Base

class Empleado(Base):
    __tablename__ = "empleados"

    # Se agrega autoincrement=True para que la BD asigne el número
    id_empleado = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido_pat = Column(String(100))
    apellido_mat = Column(String(100))
    correo = Column(String(100), unique=True)
    telefono = Column(String(15))