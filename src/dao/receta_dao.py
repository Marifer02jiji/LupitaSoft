from src.database.db_config import SessionLocal
from src.models.receta import Receta

class RecetaDAO:
    def __init__(self):
        self.db = SessionLocal()

    # --- CREATE (C) ---
    def crear_receta(self, id_sabor, id_usuario, tipo, litros, estabilizantes, descripcion):
        """Registra una nueva fórmula de producción para un sabor"""
        nueva_receta = Receta(
            id_sabor=id_sabor,
            id_usuario=id_usuario,
            tipo_receta=tipo,
            litros=litros,
            estabilizantes=estabilizantes,
            descripcion=descripcion
        )
        self.db.add(nueva_receta)
        self.db.commit()
        return nueva_receta

    # --- READ (R) ---
    def obtener_por_sabor(self, id_sabor):
        """Busca la receta específica vinculada a un sabor"""
        return self.db.query(Receta).filter(Receta.id_sabor == id_sabor).first()

    def listar_todas(self):
        """Muestra todas las recetas registradas en el sistema"""
        return self.db.query(Receta).all()

    # --- UPDATE (U) ---
    def actualizar_receta(self, id_sabor, nuevos_datos):
        """Modifica cantidades o ingredientes de una receta existente"""
        receta = self.obtener_por_sabor(id_sabor)
        if receta:
            receta.id_usuario = nuevos_datos.get('id_usuario', receta.id_usuario)
            receta.tipo_receta = nuevos_datos.get('tipo', receta.tipo_receta)
            receta.litros = nuevos_datos.get('litros', receta.litros)
            receta.estabilizantes = nuevos_datos.get('estabilizantes', receta.estabilizantes)
            receta.descripcion = nuevos_datos.get('descripcion', receta.descripcion)
            self.db.commit()
            return True
        return False

    # --- DELETE (D) ---
    def eliminar_receta(self, id_sabor):
        """Elimina físicamente una receta (usar con precaución)"""
        receta = self.obtener_por_sabor(id_sabor)
        if receta:
            self.db.delete(receta)
            self.db.commit()
            return True
        return False