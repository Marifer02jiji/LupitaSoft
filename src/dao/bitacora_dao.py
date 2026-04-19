from src.database.db_config import SessionLocal
from src.models.bitacora_inventario import BitacoraInventario

class BitacoraDAO:
    def __init__(self):
        self.db = SessionLocal()

    def registrar_movimiento(self, id_user, tipo, cant, comentario, id_sabor=None, id_insumo=None):
        try:
            movimiento = BitacoraInventario(
                id_usuario=id_user, id_sabor=id_sabor, id_insumo=id_insumo,
                tipo_movimiento=tipo, cantidad=cant, comentarios=comentario
            )
            self.db.add(movimiento)
            self.db.commit()
        finally:
            SessionLocal.remove()