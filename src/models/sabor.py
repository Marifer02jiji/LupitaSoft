from sqlalchemy import Column, Integer, String, Float, Boolean
from src.database.db_config import Base

class Sabor(Base):
    __tablename__ = "sabores"

    id_sabor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    categoria = Column(String(20))
    precio_unitario = Column(Float)
    estatus = Column(Boolean, default=True)
    # Nuevo atributo: Guardaremos el nombre del archivo (ej: "1.png")
    imagen = Column(String(100), default="default.png")