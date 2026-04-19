import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.constants import *
from src.dao.sabor_dao import SaborDAO
from src.dao.pedido_dao import PedidoDAO
from src.dao.bitacora_dao import BitacoraDAO
from PIL import Image, ImageTk
import os
from PIL import Image, ImageTk

class VentasView(tk.Frame):
    def __init__(self, parent, id_usuario):
        super().__init__(parent, bg=FONDO)
        self.id_usuario = id_usuario
        self._init_ui()

    def _init_ui(self):
        # Encabezado (Tu diseño original)

        # --- TABLA SUPERIOR (Como en tu imagen 1) ---
        cols = ("Sabor", "Cantidad", "Precio unit.", "Total", "Tipo", "Fecha")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, anchor="center")
        self.tabla.pack(fill="both", expand=True, pady=(0, 15))

        # --- FORMULARIO INFERIOR (Contenedor Lila) ---
        form_f = tk.Frame(self, bg=MORADO_CLARO, highlightbackground=MORADO_MED, highlightthickness=1)
        form_f.pack(fill="x", side="bottom", pady=10)
        
        form = tk.Frame(form_f, bg=MORADO_CLARO)
        form.pack(pady=15)

        labels = ["Sabor", "Cantidad", "Precio unitario", "Tipo", "Fecha (YYYY-MM-DD)"]
        self.entradas = []
        for i, l in enumerate(labels):
            tk.Label(form, text=l, bg=MORADO_CLARO, fg=TEXTO_OSCURO, font=("Arial", 9, "bold")).grid(row=0, column=i, padx=5)
            e = tk.Entry(form, width=15, relief="flat", highlightbackground=MORADO, highlightthickness=1)
            e.grid(row=1, column=i, padx=5, pady=5)
            self.entradas.append(e)

        # Botón Registrar Morado
        tk.Button(form, text="✔ Registrar", bg=MORADO, fg=BLANCO, font=("Arial", 10, "bold"),
                  relief="flat", cursor="hand2", padx=20, pady=8).grid(row=1, column=len(labels), padx=15)
    def _cargar_sabores(self):
        """Carga los nombres y precios de los sabores activos desde la base de datos"""
        sabores = self.sab_dao.listar_activos()
        self.lista_nombres = [s.nombre for s in sabores]
        # Mapeamos nombre -> (id, precio)
        self.dict_datos = {s.nombre: (s.id_sabor, s.precio_unitario) for s in sabores}

    def _actualizar_formulario(self):
        """Reconstruye los campos dependiendo de si es Personal o Evento"""
        for w in self.form_container.winfo_children(): w.destroy()
        
        # Campos de Sabor y Precio (Comunes)
        tk.Label(self.form_container, text="Sabor:", bg=MORADO_CLARO).grid(row=0, column=0, padx=10, pady=10)
        self.cb_sabor = ttk.Combobox(self.form_container, values=self.lista_nombres, state="readonly")
        self.cb_sabor.grid(row=0, column=1, padx=10)
        self.cb_sabor.bind("<<ComboboxSelected>>", self._on_sabor_selected)

        tk.Label(self.form_container, text="Precio Unit.:", bg=MORADO_CLARO).grid(row=0, column=2, padx=10)
        self.lbl_precio = tk.Label(self.form_container, text="$0.00", bg=MORADO_CLARO, font=("Arial", 10, "bold"))
        self.lbl_precio.grid(row=0, column=3, padx=10)

        if self.tipo_var.get() == "Evento":
            # Campos extra requeridos por el manual de usuarios
            tk.Label(self.form_container, text="Fecha Evento:", bg=MORADO_CLARO).grid(row=1, column=0, pady=10)
            self.ent_fecha = tk.Entry(self.form_container)
            self.ent_fecha.grid(row=1, column=1)

            tk.Label(self.form_container, text="Anticipo $:", bg=MORADO_CLARO).grid(row=1, column=2)
            self.ent_anticipo = tk.Entry(self.form_container)
            self.ent_anticipo.grid(row=1, column=3)

        tk.Button(self.form_container, text="REGISTRAR " + self.tipo_var.get().upper(), 
                  bg=TURQUESA, fg=BLANCO, font=("Arial", 10, "bold"),
                  command=self._procesar_venta).grid(row=2, column=1, columnspan=2, pady=20)

    def _on_sabor_selected(self, event):
        # 1. Obtener el nombre del sabor desde el Combobox
        nombre_sabor = self.cb_sabor.get()
        
        # 2. Obtener los datos (ID, Precio, Imagen) que guardamos en el diccionario
        # (Asegúrate de que tu DAO traiga el campo 'imagen' de la BD)
        datos = self.dict_datos.get(nombre_sabor)
        
        if datos:
            id_sabor, precio, nombre_img = datos # Ejemplo de lo que trae tu DAO
            
            # 3. Actualizar el precio en la pantalla
            self.lbl_precio.config(text=f"${precio:.2f}")
            
            # 4. LLAMAR A LA FUNCIÓN DE CARGA AQUÍ
            self._cargar_imagen_sabor(nombre_img)

    def _procesar_venta(self):
        nombre_sabor = self.cb_sabor.get()
        if not nombre_sabor:
            messagebox.showwarning("Atención", "Seleccione un sabor.")
            return

        id_sabor, precio = self.dict_datos[nombre_sabor]
        tipo = self.tipo_var.get()

        try:
            if tipo == "Personal":
                # Registro en tabla PedidoPersonal
                self.ped_dao.registrar_venta_mostrador(self.id_usuario, id_sabor, "Vaso/Cono", precio)
                # Registro en Bitácora (Auditoría)
                self.bit_dao.registrar_movimiento(self.id_usuario, "VENTA_MOSTRADOR", 1, 
                                                f"Venta de {nombre_sabor}", id_sabor=id_sabor)
            else:
                # Lógica para PedidoEvento
                datos_evento = {
                    "id_usuario": self.id_usuario,
                    "id_sabor": id_sabor,
                    "fecha_entrega": self.ent_fecha.get(),
                    "total_a_pagar": precio * 19, # Ejemplo: un bote de 19L
                    "anticipo": float(self.ent_anticipo.get())
                }
                self.ped_dao.registrar_evento(datos_evento)
                self.bit_dao.registrar_movimiento(self.id_usuario, "VENTA_EVENTO", 1, 
                                                f"Evento programado: {nombre_sabor}", id_sabor=id_sabor)

            messagebox.showinfo("LupitaSoft", "Operación exitosa y registrada en bitácora.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
            

    def _actualizar_imagen_sabor(self, nombre_imagen_db):
        try:
            # Buscamos en tu carpeta de imágenes
            path = f"src/static/images/{nombre_imagen_db}"
            img = Image.open(path).resize((120, 120), Image.LANCZOS)
            self.img_label.render = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.img_label.render)
        except:
            self.img_label.config(image="", text="🍧")
            
    def _cargar_imagen_sabor(self, nombre_archivo):
        
        try:
            # 1. Definir rutas
            ruta_carpeta = os.path.join("src", "static", "images")
            ruta_objetivo = os.path.join(ruta_carpeta, nombre_archivo if nombre_archivo else "")
            ruta_default = os.path.join(ruta_carpeta, "default.png")

            # 2. Lógica de selección: ¿Existe el archivo solicitado?
            if nombre_archivo and os.path.exists(ruta_objetivo):
                ruta_final = ruta_objetivo
            elif os.path.exists(ruta_default):
                ruta_final = ruta_default
            else:
                # Si ni siquiera existe default.png, usamos un placeholder vacío
                self.lbl_imagen.config(image="", text="\nLupita Helados")
                return

            # 3. Procesamiento con Pillow
            img = Image.open(ruta_final).resize((140, 140), Image.LANCZOS)
            self.foto_sabor = ImageTk.PhotoImage(img) # Guardamos referencia para evitar el GC
            
            # 4. Mostrar en la UI
            self.lbl_imagen.config(image=self.foto_sabor, text="")

        except Exception as e:
            print(f"Error crítico cargando imagen: {e}")
            self.lbl_imagen.config(image="", text="\nError UI")