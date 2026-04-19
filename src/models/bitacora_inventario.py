from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from src.database.db_config import Base
from datetime import datetime

class BitacoraInventario(Base):
    __tablename__ = "bitacora_inventario"

    id_movimiento = Column(Integer, primary_key=True, index=True) # PK 
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario")) # FK 
    id_sabor = Column(Integer, ForeignKey("sabores.id_sabor"), nullable=True) # FK 
    id_insumo = Column(Integer, ForeignKey("inventario_insumos.id_insumo"), nullable=True) # FK 
    
    # Atributos propios 
    tipo_movimiento = Column(String(50)) # Entrada, Salida o Merma
    cantidad = Column(Float)
    fecha_movimiento = Column(DateTime, default=datetime.now)
    comentarios = Column(Text)