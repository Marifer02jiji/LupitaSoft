from src.database.db_config import engine, Base

# --- IMPORTACIÓN DE TODOS LOS MODELOS ---
# Es vital importar cada uno para que SQLAlchemy los registre antes de crear las tablas
from src.models.empleado import Empleado
from src.models.usuario import Usuario
from src.models.sabor import Sabor
from src.models.receta import Receta
from src.models.inventario_insumos import InventarioInsumo
from src.models.inventario_botes import InventarioBote
from src.models.pedido_personal import PedidoPersonal
from src.models.pedido_evento import PedidoEvento
from src.models.bitacora_inventario import BitacoraInventario

def crear_base_de_datos():
    """
    Función para inicializar el esquema de la base de datos LupitaSoft.
    Crea las tablas y define las relaciones (FK) automáticamente.
    """
    print("--------------------------------------------------")
    print(" Iniciando creación de tablas en LupitaSoft DB...")
    print("--------------------------------------------------")
    
    try:
        # Esta instrucción es la que hace la magia de ingeniería
        Base.metadata.create_all(bind=engine)
        
        print(" ¡Éxito! Las siguientes tablas han sido creadas/verificadas:")
        print("   - empleados")
        print("   - usuarios")
        print("   - sabores")
        print("   - recetas")
        print("   - inventario_insumos")
        print("   - inventario_botes")
        print("   - pedidos_personal")
        print("   - pedidos_evento")
        print("   - bitacora")
        print("--------------------------------------------------")
        
    except Exception as e:
        print(f" ERROR al crear las tablas: {e}")
        print("Asegúrate de que el servicio de MySQL esté activo y tus credenciales sean correctas.")

if __name__ == "__main__":
    crear_base_de_datos()