from src.database.db_config import SessionLocal
from src.models.sabor import Sabor

class SaborDAO:
    def __init__(self):
        self.db = SessionLocal()

    # --- CREATE (C) ---
    def crear_sabor(self, nombre, categoria, precio, imagen="default.png"):
        """Registra un nuevo sabor en el catálogo"""
        nuevo = Sabor(
            nombre=nombre,
            categoria=categoria,
            precio_unitario=precio,
            imagen=imagen,
            estatus=True
        )
        self.db.add(nuevo)
        self.db.commit()
        return nuevo

    # --- READ (R) ---
    def listar_activos(self):
        """Muestra solo los sabores que están a la venta actualmente"""
        return self.db.query(Sabor).filter(Sabor.estatus == True).all()

    def obtener_por_id(self, id_sabor):
        """Busca un sabor específico por su llave primaria"""
        return self.db.query(Sabor).get(id_sabor)

    def contar_sabores(self):
        try:
            return self.db.query(Sabor).count()
        finally:
            # Esto devuelve la conexión al pool sin cerrarla del todo
            SessionLocal.remove()
            
            
    # --- UPDATE (U) ---
    def actualizar_sabor(self, id_sabor, nuevos_datos):
        """Actualiza cualquier campo del sabor (precio, nombre, etc.)"""
        sabor = self.obtener_por_id(id_sabor)
        if sabor:
            sabor.nombre = nuevos_datos.get('nombre', sabor.nombre)
            sabor.categoria = nuevos_datos.get('categoria', sabor.categoria)
            sabor.precio_unitario = nuevos_datos.get('precio', sabor.precio_unitario)
            sabor.imagen = nuevos_datos.get('imagen', sabor.imagen)
            self.db.commit()
            return True
        return False

    # --- DELETE (D) ---
    def desactivar_sabor(self, id_sabor):
        """Baja lógica: el sabor ya no aparece pero no se borra la historia"""
        sabor = self.obtener_por_id(id_sabor)
        if sabor:
            sabor.estatus = False
            self.db.commit()
            return True
        return False