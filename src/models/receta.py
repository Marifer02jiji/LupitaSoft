from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from src.database.db_config import Base

class Receta(Base):
    __tablename__ = "recetas"

    id_receta = Column(Integer, primary_key=True, index=True)
    id_sabor = Column(Integer, ForeignKey("sabores.id_sabor"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    tipo_receta = Column(String(20)) # Nieve / Helado
    litros = Column(Float)           # Leche o Agua
    estabilizantes = Column(String(50)) # DPO / DDF
    descripcion = Column(Text)