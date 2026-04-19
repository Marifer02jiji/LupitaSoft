from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from src.database.db_config import Base

# --- PEDIDO MOSTRADOR ---
class PedidoPersonal(Base):
    __tablename__ = "pedidos_personal"

    id_ped_personal = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_sabor = Column(Integer, ForeignKey("sabores.id_sabor"))
    fecha_venta = Column(DateTime)
    tipo_helado = Column(String(20))
    total_a_pagar = Column(Float)

