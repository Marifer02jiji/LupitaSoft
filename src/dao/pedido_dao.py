from src.database.db_config import SessionLocal
from src.models.pedido_personal import PedidoPersonal
from src.models.pedido_evento import PedidoEvento
from sqlalchemy import func
from datetime import date

class PedidoDAO:
    def __init__(self):
        self.db = SessionLocal()

    # --- PEDIDO PERSONAL (Mostrador) ---
    def registrar_venta_mostrador(self, id_user, id_sabor, tipo, total):
        """C: Registra una venta rápida de helado o nieve"""
        nueva_venta = PedidoPersonal(
            id_usuario=id_user, 
            id_sabor=id_sabor, 
            tipo_helado=tipo, 
            total_a_pagar=total
        )
        self.db.add(nueva_venta)
        self.db.commit()
        return nueva_venta

    def sumar_ventas_hoy(self):
        """Función Especial: Para la tarjeta turquesa del Dashboard"""
        hoy = date.today()
        total = self.db.query(func.sum(PedidoPersonal.total_a_pagar)).filter(
            func.date(PedidoPersonal.fecha_venta) == hoy
        ).scalar()
        return total if total else 0.0

    # --- PEDIDO EVENTO (Logística) ---
    def registrar_evento(self, datos):
        """C: Guarda un nuevo contrato para evento (Tec Toluca, fiestas, etc.)"""
        nuevo_evento = PedidoEvento(**datos)
        self.db.add(nuevo_evento)
        self.db.commit()
        return nuevo_evento

    def listar_eventos_pendientes(self):
        """R: Muestra eventos cuya fecha es hoy o futura"""
        return self.db.query(PedidoEvento).filter(PedidoEvento.fecha_evento >= date.today()).all()

    def actualizar_estatus_evento(self, id_evento, nuevo_estatus):
        """U: Permite marcar eventos como 'Pagado' o 'Entregado'"""
        evento = self.db.query(PedidoEvento).get(id_evento)
        if evento:
            # Aquí podrías añadir un campo estatus si lo agregaste al modelo
            self.db.commit()
            return True
        return False
