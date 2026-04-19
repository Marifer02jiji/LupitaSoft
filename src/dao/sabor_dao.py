from src.database.db_config import SessionLocal
from src.models.sabor import Sabor

class SaborDAO:
    def __init__(self):
        self.db = SessionLocal()

    def listar_activos(self):
        """Muestra solo los sabores con estatus True en la galería y tabla"""
        try:
            return self.db.query(Sabor).filter(Sabor.estatus == True).all()
        finally:
            SessionLocal.remove()

    def crear_sabor(self, nombre, categoria, precio, imagen="default.png"):
        try:
            nuevo = Sabor(
                nombre=nombre,
                categoria=categoria,
                precio_unitario=precio,
                imagen=imagen,
                estatus=True
            )
            self.db.add(nuevo)
            self.db.commit()
            self.db.refresh(nuevo) # Esto recupera el ID generado por la BD
            return nuevo # <-- Importante devolver el objeto
        except Exception as e:
            self.db.rollback()
            raise e

    def actualizar_sabor(self, id_sabor, datos):
        try:
            sabor = self.db.query(Sabor).filter(Sabor.id_sabor == id_sabor).first()
            if sabor:
                sabor.nombre = datos.get('nombre', sabor.nombre)
                sabor.categoria = datos.get('categoria', sabor.categoria)
                sabor.precio_unitario = datos.get('precio', sabor.precio_unitario)
                sabor.imagen = datos.get('imagen', sabor.imagen)
                self.db.commit()
                return True
            return False
        finally:
            SessionLocal.remove()

    def desactivar_sabor(self, id_sabor):
        """Baja lógica para no perder historial de ventas"""
        try:
            sabor = self.db.query(Sabor).filter(Sabor.id_sabor == id_sabor).first()
            if sabor:
                sabor.estatus = False
                self.db.commit()
                return True
            return False
        finally:
            SessionLocal.remove()

    def contar_sabores(self):
        try:
            return self.db.query(Sabor).filter(Sabor.estatus == True).count()
        finally:
            SessionLocal.remove()