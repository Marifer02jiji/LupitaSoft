import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from src.ui.constants import *

class RecetaView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=FONDO)
        self._verificar_acceso()

    def _verificar_acceso(self):
        # El código secreto que definimos en tu manual
        codigo = simpledialog.askstring("Seguridad", "Ingrese código de cocina:", show='*')
        if codigo == "LUPITA1979":
            self._init_ui()
        else:
            messagebox.showerror("Error", "Código incorrecto. Acceso denegado.")
            tk.Label(self, text="🔒 Acceso Restringido", font=FONT_TITULO, bg=FONDO).pack(expand=True)

    def _init_ui(self):
        # ENCABEZADO TURQUESA (Diseño Imagen 3)
        header = tk.Frame(self, bg=TURQUESA_CLARO, highlightbackground=TURQUESA, highlightthickness=1)
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="👨‍🍳 Panel de Producción", font=FONT_TITULO, 
                 bg=TURQUESA_CLARO, fg=TURQUESA).pack(side="left", padx=20, pady=15)

        # --- SECCIÓN RECETAS ---
        tk.Label(self, text="📖 Recetario Maestro", font=FONT_SUB, bg=FONDO, fg=MORADO).pack(anchor="w")
        self.tabla_recetas = ttk.Treeview(self, columns=("Sabor", "Base", "Rendimiento"), show="headings", height=5)
        self.tabla_recetas.heading("Sabor", text="Sabor"); self.tabla_recetas.heading("Base", text="Base"); self.tabla_recetas.heading("Rendimiento", text="Rendimiento")
        self.tabla_recetas.pack(fill="x", pady=(5, 20))

        # --- SECCIÓN INVENTARIO (SEMÁFORO) ---
        tk.Label(self, text="📦 Estado de Insumos", font=FONT_SUB, bg=FONDO, fg=MORADO).pack(anchor="w")
        self.tabla_inv = ttk.Treeview(self, columns=("Insumo", "Stock", "Estado"), show="headings", height=8)
        self.tabla_inv.heading("Insumo", text="Insumo"); self.tabla_inv.heading("Stock", text="Cantidad"); self.tabla_inv.heading("Estado", text="Estado")
        self.tabla_inv.pack(fill="x", pady=5)
        
        # Ejemplo de semáforo
        self.tabla_inv.insert("", "end", values=("Leche Entera", "5L", "CRÍTICO"), tags=('bajo',))
        self.tabla_inv.tag_configure('bajo', foreground="red")