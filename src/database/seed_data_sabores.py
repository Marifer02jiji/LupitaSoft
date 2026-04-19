from src.database.db_config import SessionLocal
from src.models.sabor import Sabor

def cargar_todos_los_sabores():
    db = SessionLocal()
    print(" Iniciando la carga masiva con imágenes para Helados Lupita...")

    # Lista completa basada en 'Helados en existencia.docx' [cite: 1]
    datos_sabores = [
        # --- AGUA (Nieves) [cite: 2] ---
        {"nombre": "Tamarindo", "cat": "Nieve"}, {"nombre": "Limón", "cat": "Nieve"},
        {"nombre": "Mango con chile", "cat": "Nieve"}, {"nombre": "Zapote", "cat": "Nieve"},
        {"nombre": "Frutos rojos", "cat": "Nieve"}, {"nombre": "Manzana verde", "cat": "Nieve"},
        {"nombre": "Maracuyá", "cat": "Nieve"}, {"nombre": "Pica fresa", "cat": "Nieve"},
        {"nombre": "Icce de Cereza", "cat": "Nieve"}, {"nombre": "Guanábana", "cat": "Nieve"},

        # --- LECHE - CHOCOLATOSOS [cite: 14] ---
        {"nombre": "Ferrero", "cat": "Helado"}, {"nombre": "Chocolate Hershey", "cat": "Helado"},
        {"nombre": "Chocolate Abuelita", "cat": "Helado"}, {"nombre": "Selva Negra", "cat": "Helado"},
        {"nombre": "Kinder Bueno", "cat": "Helado"}, {"nombre": "Chocomenta", "cat": "Helado"},
        {"nombre": "Kinder Delice", "cat": "Helado"}, {"nombre": "Gansito", "cat": "Helado"},
        {"nombre": "Bubulubu", "cat": "Helado"}, {"nombre": "Chocochips", "cat": "Helado"},
        {"nombre": "Galleta Oreo", "cat": "Helado"},

        # --- LECHE - FRUTALES [cite: 26] ---
        {"nombre": "Crema de limón", "cat": "Helado"}, {"nombre": "Crema de naranja", "cat": "Helado"},
        {"nombre": "Crema de piña", "cat": "Helado"}, {"nombre": "Crema de mandarina", "cat": "Helado"},
        {"nombre": "Crema de fresa", "cat": "Helado"}, {"nombre": "Crema de higo", "cat": "Helado"},
        {"nombre": "Crema de coco", "cat": "Helado"}, {"nombre": "Crema de Mango", "cat": "Helado"},
        {"nombre": "Frutas secas", "cat": "Helado"}, {"nombre": "Crema de Lima", "cat": "Helado"},
        {"nombre": "Frutos del bosque", "cat": "Helado"}, {"nombre": "Mamey", "cat": "Helado"},
        {"nombre": "Guayaba", "cat": "Helado"}, {"nombre": "Cereza", "cat": "Helado"},
        {"nombre": "Nanche", "cat": "Helado"}, {"nombre": "Beso de Ángel", "cat": "Helado"},

        # --- LECHE - CREMOSOS / QUESOS [cite: 43] ---
        {"nombre": "Flor de nata", "cat": "Helado"}, {"nombre": "Chongos Queso Zamoranos", "cat": "Helado"},
        {"nombre": "Tres leches", "cat": "Helado"}, {"nombre": "Queso con Zarzamora", "cat": "Helado"},
        {"nombre": "Queso Cotija", "cat": "Helado"}, {"nombre": "Queso Philadelphia", "cat": "Helado"},
        {"nombre": "Cajeta", "cat": "Helado"},

        # --- LECHE - SEMILLAS [cite: 51] ---
        {"nombre": "Nuez", "cat": "Helado"}, {"nombre": "Pistache", "cat": "Helado"},
        {"nombre": "Almendra", "cat": "Helado"}, {"nombre": "Piñón", "cat": "Helado"},
        {"nombre": "Mazapán", "cat": "Helado"},

        # --- LECHE - BEBIDAS [cite: 57] ---
        {"nombre": "Baileys", "cat": "Helado"}, {"nombre": "Ron con pasas", "cat": "Helado"},
        {"nombre": "Amaretto", "cat": "Helado"}, {"nombre": "Buchanan’s", "cat": "Helado"},
        {"nombre": "Crema de tequila", "cat": "Helado"}, {"nombre": "Piña colada", "cat": "Helado"},
        {"nombre": "Rompope", "cat": "Helado"}, {"nombre": "Martell", "cat": "Helado"},

        # --- LECHE - DULCES Y CAFÉ [cite: 66] ---
        {"nombre": "Vainilla", "cat": "Helado"}, {"nombre": "Tiramisú", "cat": "Helado"},
        {"nombre": "Nescafé", "cat": "Helado"}, {"nombre": "Algodón de azúcar", "cat": "Helado"},
        {"nombre": "Chicle", "cat": "Helado"}, {"nombre": "Pay de limón", "cat": "Helado"}
    ]

    try:
        agregados = 0
        # Usamos enumerate para generar el número de la imagen automáticamente
        for i, item in enumerate(datos_sabores):
            # Evitar duplicados
            existe = db.query(Sabor).filter(Sabor.nombre == item["nombre"]).first()
            if not existe:
                # El nombre de la imagen será el número de posición + 1 (ej: 1.png, 2.png)
                nombre_imagen = f"{i+1}.png"
                
                nuevo = Sabor(
                    nombre=item["nombre"],
                    categoria=item["cat"],
                    precio_unitario=40.0, # Precio base [cite: 73]
                    estatus=True,
                    imagen=nombre_imagen
                )
                db.add(nuevo)
                agregados += 1
        
        db.commit()
        print(f" ¡Éxito! Se agregaron {agregados} sabores con sus respectivas imágenes.")
    except Exception as e:
        db.rollback()
        print(f" Error durante la carga: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cargar_todos_los_sabores()