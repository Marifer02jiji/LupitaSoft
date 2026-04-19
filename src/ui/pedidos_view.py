import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.constants import *
from src.dao.pedido_dao import PedidoDAO

class PedidosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=FONDO)
        self.dao = PedidoDAO()
        self._init_ui()

    def _init_ui(self):
        # Título con tipografía Georgia e itálica como tu diseño original
        tk.Label(self, text="🛒 Logística de Pedidos Especiales (Eventos)", 
                 font=("Georgia", 16, "bold italic"), bg=FONDO, fg=MORADO).pack(anchor="w", pady=(0, 15))

        # --- TABLA DE LOGÍSTICA (Diseño de Imagen 2) ---
        columnas = ("ID", "Cliente", "Teléfono", "Sabor/Cantidad", "Total", "Anticipo", "Entrega", "Estado")
        
        # Estilo para la tabla (ttk)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))
        
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=15)
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=120)
        
        self.tabla.pack(fill="both", expand=True)

        # Barra de botones de acción rápida
        btn_frame = tk.Frame(self, bg=FONDO)
        btn_frame.pack(fill="x", pady=20)

        # Botones con tu estilo original (Turquesa y Morado)
        self._btn(btn_frame, "✅ Marcar Entregado", TURQUESA).pack(side="left", padx=5)
        self._btn(btn_frame, "📞 Contactar Cliente", MORADO).pack(side="left", padx=5)
        self._btn(btn_frame, "🔄 Actualizar Lista", TURQUESA_MED).pack(side="right", padx=5)

        # --- PIE DE PÁGINA (Amarillo Pastel de tu imagen 2) ---
        footer = tk.Frame(self, bg=AMARILLO_PASTEL, highlightthickness=1, highlightbackground="#f0d080")
        footer.pack(fill="x", pady=(10, 0))
        tk.Label(footer, text="📌 Los pedidos en 'Pendiente' con fecha de hoy aparecen resaltados.", 
                 bg=AMARILLO_PASTEL, font=("Arial", 9, "italic")).pack(pady=8)

        self.cargar_datos()

    def _btn(self, parent, texto, color):
        return tk.Button(parent, text=texto, bg=color, fg=BLANCO, relief="flat",
                         font=("Arial", 9, "bold"), padx=15, pady=8, cursor="hand2")

    def cargar_datos(self):
        """Limpia la tabla y carga los pedidos de eventos desde el DAO"""
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        try:
            # Aquí llamamos a la función específica para eventos
            pedidos = self.dao.listar_pedidos_eventos()
            for p in pedidos:
                # El estado se puede pintar de color según la urgencia
                self.tabla.insert("", "end", values=(
                    p.id_pedido, p.cliente_nombre, p.telefono, 
                    p.sabor_nombre, f"${p.total}", f"${p.anticipo}", 
                    p.fecha_entrega, p.estado
                ))
        except Exception as e:
            print(f"Error al cargar pedidos: {e}")