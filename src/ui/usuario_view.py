import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.constants import *
from src.dao.usuario_dao import UsuarioDAO

class UsuarioView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=FONDO)
        self.dao = UsuarioDAO()
        self._init_ui()

    def _init_ui(self):
        
        # --- TABLA DE USUARIOS ---
        columnas = ("ID", "Código/Usuario", "Rol", "Nombre Completo")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=180)
        
        self.tabla.pack(fill="x", pady=10)

        # --- BOTONERA CRUD ---
        frame_botones = tk.Frame(self, bg=FONDO)
        frame_botones.pack(fill="x", pady=20)

        self._crear_btn(frame_botones, " Registrar Nuevo", TURQUESA, self._abrir_registro).pack(side="left", padx=5)
        self._crear_btn(frame_botones, " Modificar", MORADO, self._abrir_edicion).pack(side="left", padx=5)
        self._crear_btn(frame_botones, " Dar de Baja", "#e74c3c", self._eliminar).pack(side="left", padx=5)

        self._cargar_datos()

    def _crear_btn(self, parent, texto, color, comando):
        return tk.Button(parent, text=texto, bg=color, fg=BLANCO, 
                         font=("Arial", 10, "bold"), relief="flat", 
                         cursor="hand2", padx=15, pady=8, command=comando)

    def _cargar_datos(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        datos = self.dao.listar_usuarios_completo()
        for user, emp in datos:
            nombre_completo = f"{emp.nombre} {emp.apellido_pat}"
            self.tabla.insert("", "end", values=(
                user.id_empleado, 
                user.correo, 
                user.rol, 
                nombre_completo
            ))

    def _abrir_registro(self):
        self._ventana_form("crear")

    def _abrir_edicion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un usuario de la tabla.")
            return
        self._ventana_form("editar", self.tabla.item(seleccion)['values'])

    def _ventana_form(self, modo, datos=None):
        v = tk.Toplevel(self)
        v.title("LupitaSoft - Registro" if modo == "crear" else "LupitaSoft - Editar")
        v.geometry("400x600")
        v.configure(bg=MORADO_CLARO)
        v.grab_set()

        texto_titulo = " REGISTRAR NUEVO" if modo == "crear" else " EDITAR PERSONAL"
        tk.Label(v, text=texto_titulo, font=("Georgia", 12, "bold italic"), 
                 bg=MORADO_CLARO, fg=MORADO).pack(pady=15)

        f = tk.Frame(v, bg=MORADO_CLARO)
        f.pack(padx=30)

        entradas = {}
        campos = [
            ("Nombre(s):", "nombre"),
            ("Apellido Paterno:", "apellido"),
            ("Código de Acceso (Ej: HLA01):", "codigo"),
            ("Contraseña (dejar vacío para no cambiar):", "pass"),
        ]

        for label, clave in campos:
            tk.Label(f, text=label, bg=MORADO_CLARO, fg=TEXTO_OSCURO).pack(anchor="w", pady=(10, 0))
            show = "*" if clave == "pass" else None
            e = tk.Entry(f, width=35, show=show, relief="flat", highlightthickness=1, highlightbackground=MORADO_MED)
            e.pack(pady=5)
            entradas[clave] = e

        tk.Label(f, text="Rol del Sistema:", bg=MORADO_CLARO, fg=TEXTO_OSCURO).pack(anchor="w", pady=(10, 0))
        cb_rol = ttk.Combobox(f, values=["Admin", "Empleado"], state="readonly", width=32)
        cb_rol.pack(pady=5)
        cb_rol.set("Empleado")

        if modo == "editar":
            entradas["codigo"].insert(0, datos[1])
            cb_rol.set(datos[2])
            nombres = datos[3].split()
            entradas["nombre"].insert(0, nombres[0] if len(nombres) > 0 else "")
            entradas["apellido"].insert(0, nombres[1] if len(nombres) > 1 else "")

        def ejecutar_guardado():
            nom, ape, cod, pas = entradas["nombre"].get(), entradas["apellido"].get(), entradas["codigo"].get(), entradas["pass"].get()
            r = cb_rol.get()

            if not nom or not cod:
                messagebox.showwarning("Atención", "Nombre y Código son obligatorios.")
                return

            if modo == "crear":
                exito = self.dao.registrar_personal_completo(nom, ape, cod, pas, r)
            else:
                exito = self.dao.modificar_usuario(datos[0], nom, ape, cod, pas, r)

            if exito:
                messagebox.showinfo("Éxito", "Operación exitosa")
                self._cargar_datos()
                v.destroy()
            else:
                messagebox.showerror("Error", "No se pudo completar la acción.")

        btn_txt = "REGISTRAR" if modo == "crear" else "ACTUALIZAR"
        btn_col = TURQUESA if modo == "crear" else MORADO
        tk.Button(v, text=btn_txt, bg=btn_col, fg=BLANCO, font=("Arial", 10, "bold"),
                  padx=20, pady=12, command=ejecutar_guardado).pack(pady=30)

    def _eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un usuario.")
            return
        
        id_emp = self.tabla.item(seleccion)['values'][0]
        nombre = self.tabla.item(seleccion)['values'][3]

        if messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente a {nombre}?"):
            if self.dao.eliminar_usuario_completo(id_emp):
                messagebox.showinfo("Éxito", "Usuario eliminado.")
                self._cargar_datos()