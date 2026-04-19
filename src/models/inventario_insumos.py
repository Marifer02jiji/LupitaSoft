from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from src.database.db_config import Base

# --- INSUMOS ---
class InventarioInsumo(Base):
    __tablename__ = "inventario_insumos"

    id_insumo = Column(Integer, primary_key=True, index=True)
    nombre_insumo = Column(String(50)) # Servilletas, Conos, etc.
    estatus = Column(String(20))
    cantidad_actual = Column(Float)
    stock_minimo = Column(Float)
    unidad_medida = Column(String(20))

