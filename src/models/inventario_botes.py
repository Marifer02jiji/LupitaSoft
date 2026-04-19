from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from src.database.db_config import Base

# --- BOTES DE HELADO ---
class InventarioBote(Base):
    __tablename__ = "inventario_botes"

    id_bote = Column(Integer, primary_key=True, index=True)
    id_sabor = Column(Integer, ForeignKey("sabores.id_sabor"))
    numero_bote = Column(Integer)
    estatus = Column(String(20))
    fecha_caducidad = Column(Date) # Alerta roja
    fecha_entrada = Column(Date)
    ubicacion = Column(String(50))