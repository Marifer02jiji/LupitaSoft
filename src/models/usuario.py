from sqlalchemy import Column, Integer, String, ForeignKey
from src.database.db_config import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    # ID de control interno autoincremental
    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Llave foránea que apunta al ID numérico del empleado
    id_empleado = Column(Integer, ForeignKey("empleados.id_empleado"))
    
    rol = Column(String(20)) # Admin / Empleado
    contrasena = Column(String(100), nullable=False)
    
    # Aquí es donde guardarás el código HLA01, HLE02, etc.
    correo = Column(String(100), unique=True)