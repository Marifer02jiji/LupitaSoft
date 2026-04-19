import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.constants import *
from src.dao.sabor_dao import SaborDAO

class SaborView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=FONDO)
        self.dao = SaborDAO()
        self._init_ui()

    def _init_ui(self):
        tk.Label(self, text="🍦 Catálogo de Sabores", font=("Georgia", 18, "bold italic"),
                 bg=FONDO, fg=MORADO).pack(anchor="w", padx=30, pady=20)

        # Tabla de Sabores
        cols = ("ID", "Nombre", "Categoría", "Precio", "Estatus")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=120, anchor="center")
        self.tabla.pack(fill="x", padx=30)

        # Formulario de Edición Rápida
        edit_frame = tk.LabelFrame(self, text=" Gestión de Sabor ", bg=FONDO, fg=TEXTO_OSCURO)
        edit_frame.pack(fill="x", padx=30, pady=20)

        tk.Label(edit_frame, text="Nuevo Precio:", bg=FONDO).grid(row=0, column=0, padx=10, pady=10)
        self.ent_precio = tk.Entry(edit_frame)
        self.ent_precio.grid(row=0, column=1)

        tk.Button(edit_frame, text="Actualizar Precio", bg=TURQUESA, fg=BLANCO, 
                  command=self._actualizar).grid(row=0, column=2, padx=20)
        
        self._cargar_datos()

    def _cargar_datos(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        for s in self.dao.listar_activos():
            est = "✅ Activo" if s.estatus else "❌ Inactivo"
            self.tabla.insert("", "end", values=(s.id_sabor, s.nombre, s.categoria, f"${s.precio_unitario}", est))

    def _actualizar(self):
        item = self.tabla.selection()
        if not item:
            messagebox.showwarning("Atención", "Selecciona un sabor de la tabla.")
            return
        
        id_s = self.tabla.item(item)['values'][0]
        try:
            nuevo_p = float(self.ent_precio.get())
            self.dao.actualizar_sabor(id_s, {"precio": nuevo_p})
            messagebox.showinfo("Éxito", "Precio actualizado correctamente.")
            self._cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido para el precio.")