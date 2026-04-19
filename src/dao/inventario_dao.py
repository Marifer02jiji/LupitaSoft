from src.database.db_config import SessionLocal
from src.models.inventario_insumos import InventarioInsumo
from src.models.inventario_botes import InventarioBote
from datetime import date, timedelta

class InventarioDAO:
    def __init__(self):
        self.db = SessionLocal()

    def listar_insumos(self):
        try:
            return self.db.query(InventarioInsumo).all()
        finally:
            SessionLocal.remove()
    def guardar_insumo(self, nombre, cantidad, minimo, unidad):
        try: 
            insumo = self.db.query(InventarioInsumo).filter(InventarioInsumo.nombre_insumo == nombre).first()
            if not insumo:
                insumo = InventarioInsumo(nombre_insumo=nombre)
                self.db.add(insumo)
            
            insumo.cantidad_actual = cantidad
            insumo.stock_minimo = minimo
            insumo.unidad_medida = unidad
            self.db.commit()
        finally:
            SessionLocal.remove()
    def contar_bajo_stock(self):
        try:
            return self.db.query(InventarioInsumo).filter(
                InventarioInsumo.cantidad_actual <= InventarioInsumo.stock_minimo
            ).count()
        finally:
            SessionLocal.remove()
            
            
    # --- INVENTARIO BOTES (Producto Terminado) ---
    def registrar_bote(self, id_sabor, num_bote, fecha_cad, ubicacion):
        try:        
            nuevo_bote = InventarioBote(
                id_sabor=id_sabor,
                numero_bote=num_bote,
                fecha_caducidad=fecha_cad,
                ubicacion=ubicacion,
                estatus="Disponible"
            )
            self.db.add(nuevo_bote)
            self.db.commit()
        finally:
            SessionLocal.remove()
    def obtener_botes_con_alerta(self):
        try:
            limite = date.today() + timedelta(days=2)
            return self.db.query(InventarioBote).filter(
                InventarioBote.fecha_caducidad <= limite,
                InventarioBote.estatus == "Disponible"
            ).all()
        finally:
            SessionLocal.remove()
            
    def cambiar_estatus_bote(self, id_bote, nuevo_estatus):
        try:
            
            bote = self.db.query(InventarioBote).get(id_bote)
            if bote:
                bote.estatus = nuevo_estatus
                self.db.commit()
                return True
            return False
        finally:
            SessionLocal.remove()