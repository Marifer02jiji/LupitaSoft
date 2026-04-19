from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from src.database.db_config import Base

# --- PEDIDO EVENTOS ---
class PedidoEvento(Base):
    __tablename__ = "pedidos_evento"

    id_ped_evento = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_sabor = Column(Integer, ForeignKey("sabores.id_sabor"))
    fecha_evento = Column(Date)
    hora = Column(String(10))
    lugar_entrega = Column(String(200))
    cantidad_litros = Column(Float)
    num_personas = Column(Integer)
    numero_despachadores = Column(Integer)