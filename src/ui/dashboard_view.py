import tkinter as tk
from src.ui.constants import *
from src.dao.sabor_dao import SaborDAO
from src.dao.inventario_dao import InventarioDAO
from src.dao.pedido_dao import PedidoDAO

class DashboardView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=FONDO)
        # Inicialización de DAOs
        self.sabor_dao = SaborDAO()
        self.inv_dao = InventarioDAO()
        self.ped_dao = PedidoDAO()
        self._init_ui()

    def _init_ui(self):
        # Título estilo Georgia original
        tk.Label(self, text="📊 Dashboard Informativo", font=("Georgia", 18, "bold italic"),
                 bg=FONDO, fg=MORADO).pack(anchor="w", padx=30, pady=30)

        # 1. CONSULTAS A LA BASE DE DATOS
        # Usamos bloques try/except por si la base de datos está vacía al inicio
        try:
            ventas_hoy = self.ped_dao.sumar_ventas_hoy() or 0.0
            bajo_stock = self.inv_dao.contar_bajo_stock() or 0
            total_sabores = self.sabor_dao.contar_sabores() or 0
            
            # Si listar_eventos_pendientes devuelve una lista, usamos len()
            pedidos_lista = self.ped_dao.listar_eventos_pendientes()
            pedido_pendiente = len(pedidos_lista) if isinstance(pedidos_lista, list) else 0
        except Exception as e:
            print(f"Error cargando datos dashboard: {e}")
            ventas_hoy, bajo_stock, total_sabores, pedido_pendiente = 0, 0, 0, 0

        # 2. CONTENEDOR DE TARJETAS (Usamos Grid para que queden alineadas)
        contenedor = tk.Frame(self, bg=FONDO)
        contenedor.pack(fill="x", padx=30)

        # Tarjeta 1: Ventas (TURQUESA)
        self._crear_tarjeta(contenedor, 0, "Ventas Hoy", f"${ventas_hoy:.2f}", TURQUESA, TURQUESA_CLARO)
        
        # Tarjeta 2: Stock (ROSA/NARANJA)
        self._crear_tarjeta(contenedor, 1, "Stock Bajo", str(bajo_stock), "#e8a87c", "#fff3e8")
        
        # Tarjeta 3: Sabores (MORADO)
        self._crear_tarjeta(contenedor, 2, "Sabores Activos", str(total_sabores), MORADO, MORADO_CLARO)
        
        # Tarjeta 4: La faltante (AMARILLO/VERDE)
        self._crear_tarjeta(contenedor, 3, "Pedidos Pendientes", str(pedido_pendiente), "#56ab91", "#eafaf1")

    def _crear_tarjeta(self, parent, columna, titulo, valor, color_borde, color_fondo):
        """
        Crea una tarjeta con el diseño exacto de tu MAIN original:
        Borde de 2px, fondo pastel y tipografía Georgia.
        """
        # Marco exterior (el borde de 2px)
        card = tk.Frame(parent, bg=color_borde, padx=2, pady=2)
        card.grid(row=0, column=columna, padx=10, sticky="nsew")
        
        # Marco interior (el fondo pastel)
        inner = tk.Frame(card, bg=color_fondo, padx=20, pady=20, width=180, height=120)
        inner.pack(fill="both", expand=True)
        inner.pack_propagate(False) # Mantiene el tamaño fijo

        # Etiquetas de texto
        tk.Label(inner, text=titulo, font=("Arial", 10, "bold"), 
                 bg=color_fondo, fg=TEXTO_OSCURO).pack(anchor="w")
        
        tk.Label(inner, text=valor, font=("Georgia", 18, "bold"), 
                 bg=color_fondo, fg=color_borde).pack(anchor="w", pady=(10, 0))