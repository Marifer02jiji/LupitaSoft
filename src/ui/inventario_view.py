import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.constants import *
from src.dao.inventario_dao import InventarioDAO

class InventarioView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=FONDO)
        self.dao = InventarioDAO()
        self._init_ui()

    def _init_ui(self):
        
        # --- SECCIÓN INSUMOS (Semáforo) ---
        tk.Label(self, text="Materia Prima (Insumos)", font=("Arial", 11, "bold"), bg=FONDO, fg=TEXTO_OSCURO).pack(anchor="w", padx=30)
        
        cols_ins = ("Producto", "Cantidad", "Mínimo", "Estatus")
        self.tabla_ins = ttk.Treeview(self, columns=cols_ins, show="headings", height=8)
        for c in cols_ins:
            self.tabla_ins.heading(c, text=c)
            self.tabla_ins.column(c, anchor="center")
        
        self.tabla_ins.tag_configure("rojo", background="#fde8e8")
        self.tabla_ins.tag_configure("amarillo", background="#fef9e7")
        self.tabla_ins.tag_configure("verde", background="#e8fdf0")
        self.tabla_ins.pack(fill="x", padx=30, pady=(5, 20))

        # --- SECCIÓN BOTES (Alerta Roja) ---
        tk.Label(self, text="Helado Terminado (Botes 19L) - Alertas de Caducidad", font=("Arial", 11, "bold"), bg=FONDO, fg="#c0392b").pack(anchor="w", padx=30)
        
        cols_bot = ("Sabor ID", "Bote #", "Caducidad", "Ubicación")
        self.tabla_bot = ttk.Treeview(self, columns=cols_bot, show="headings", height=5)
        for c in cols_bot:
            self.tabla_bot.heading(c, text=c)
            self.tabla_bot.column(c, anchor="center")
        self.tabla_bot.tag_configure("alerta", background="#ffcccc", foreground="red")
        self.tabla_bot.pack(fill="x", padx=30, pady=5)

        self.actualizar_tablas()

    def actualizar_tablas(self):
        # 1. Cargar Insumos
        for i in self.tabla_ins.get_children(): self.tabla_ins.delete(i)
        for ins in self.dao.listar_insumos():
            if ins.cantidad_actual <= 0: tag, est = "rojo", "AGOTADO"
            elif ins.cantidad_actual <= ins.stock_minimo: tag, est = "amarillo", "STOCK BAJO"
            else: tag, est = "verde", "OK"
            self.tabla_ins.insert("", "end", values=(ins.nombre_insumo, ins.cantidad_actual, ins.stock_minimo, est), tags=(tag,))

        # 2. Cargar Botes con Alerta
        for i in self.tabla_bot.get_children(): self.tabla_bot.delete(i)
        for bot in self.dao.obtener_botes_con_alerta():
            self.tabla_bot.insert("", "end", values=(bot.id_sabor, bot.numero_bote, bot.fecha_caducidad, bot.ubicacion), tags=("alerta",))