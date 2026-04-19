from datetime import date, datetime, timedelta
from src.database.db_config import SessionLocal
from src.models.empleado import Empleado
from src.models.usuario import Usuario
from src.models.sabor import Sabor
from src.models.receta import Receta
from src.models.inventario_insumos import InventarioInsumo
from src.models.inventario_botes import InventarioBote
from src.models.bitacora_inventario import BitacoraInventario
from src.models.pedido_personal import PedidoPersonal
from src.models.pedido_evento import PedidoEvento

def cargar_datos_maestros():
    db = SessionLocal()
    print("--------------------------------------------------")
    print("🚀 Cargando datos de prueba para LupitaSoft...")
    print("--------------------------------------------------")

    try:
        # 1. EMPLEADOS (Sandra y Blanca como ejemplos del equipo)
        if not db.query(Empleado).first():
            emp1 = Empleado(nombre="Sandra", apellido_pat="Castro", apellido_mat="Segura", correo="sandra@ittol.com", telefono="7221234567")
            emp2 = Empleado(nombre="Blanca", apellido_pat="Santana", apellido_mat="S", correo="blanca@lupita.com", telefono="7229876543")
            db.add_all([emp1, emp2])
            db.commit()
            print("✅ Empleados: Registrados.")

        # 2. USUARIOS (Roles: Admin y Empleado según tu documento)
        if not db.query(Usuario).first():
            # HLA01 es Admin, HLE01 es Empleado (Cocina)
            u1 = Usuario(id_empleado=1, rol="Admin", contrasena="lupita2026", correo="HLA01")
            u2 = Usuario(id_empleado=2, rol="Empleado", contrasena="cocina123", correo="HLE01")
            db.add_all([u1, u2])
            db.commit()
            print("✅ Usuarios: HLA01 (Admin) y HLE01 (Empleado) listos.")

        # 3. RECETAS (Basadas en Sabor 1: Tamarindo y 11: Ferrero)
        if not db.query(Receta).first():
            r1 = Receta(id_sabor=1, id_usuario=2, tipo_receta="Nieve", litros=10.0, estabilizantes="DPO", descripcion="Pulpa natural base agua.")
            r2 = Receta(id_sabor=11, id_usuario=2, tipo_receta="Helado", litros=8.5, estabilizantes="DDF", descripcion="Base leche con chocolate Ferrero.")
            db.add_all([r1, r2])
            db.commit()
            print("✅ Recetas: Cargas iniciales completadas.")

        # 4. INVENTARIO INSUMOS (Control de Stock Mínimo)
        if not db.query(InventarioInsumo).first():
            i1 = InventarioInsumo(nombre_insumo="Servilletas", estatus="Suficiente", cantidad_actual=1000, stock_minimo=200, unidad_medida="Piezas")
            i2 = InventarioInsumo(nombre_insumo="Conos", estatus="Bajo", cantidad_actual=45, stock_minimo=150, unidad_medida="Piezas")
            db.add_all([i1, i2])
            db.commit()
            print("✅ Insumos: Registrados (Prueba de semáforo bajo).")

        # 5. INVENTARIO BOTES (Prueba de Alerta Roja)
        if not db.query(InventarioBote).first():
            # Bote normal
            b1 = InventarioBote(id_sabor=1, numero_bote=1, estatus="Disponible", fecha_caducidad=date.today() + timedelta(days=20), fecha_entrada=date.today(), ubicacion="Estante A")
            # Bote que caduca MAÑANA (Para pintar de rojo en la tabla)
            b2 = InventarioBote(id_sabor=11, numero_bote=1, estatus="Disponible", fecha_caducidad=date.today() + timedelta(days=1), fecha_entrada=date.today(), ubicacion="Estante B")
            db.add_all([b1, b2])
            db.commit()
            print("✅ Botes: Registrados (Incluye Alerta Roja).")

        # 6. BITÁCORA (Movimientos de inventario)
        if not db.query(BitacoraInventario).first():
            m1 = BitacoraInventario(id_usuario=1, id_sabor=1, tipo_movimiento="Entrada", cantidad=1.0, comentarios="Producción inicial.")
            db.add(m1)
            db.commit()
            print("✅ Bitácora: Movimiento inicial registrado.")

        # 7. PEDIDOS (Ventas de prueba)
        if not db.query(PedidoPersonal).first():
            p1 = PedidoPersonal(id_usuario=2, id_sabor=1, fecha_venta=datetime.now(), tipo_helado="Vaso", total_a_pagar=40.0)
            db.add(p1)
        
        if not db.query(PedidoEvento).first():
            e1 = PedidoEvento(id_usuario=1, id_sabor=11, fecha_evento=date.today() + timedelta(days=15), hora="14:00", lugar_entrega="Tec Toluca", cantidad_litros=15.0, num_personas=40, numero_despachadores=1)
            db.add(e1)
            
        db.commit()
        print("✅ Pedidos: Ventas de prueba listas.")
        print("--------------------------------------------------")
        print("✨ ¡Base de datos poblada con éxito!")

    except Exception as e:
        db.rollback()
        print(f"❌ ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cargar_datos_maestros()