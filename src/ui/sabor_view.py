import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import shutil
from tkinter import filedialog
from src.ui.constants import *
from src.dao.sabor_dao import SaborDAO

class SaborView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=FONDO)
        self.dao = SaborDAO()
        self.imagenes_refs = [] 
        # Variable para la ruta de nueva imagen
        self.ruta_nueva_img = tk.StringVar(value="")
        self._init_ui()

    def _init_ui(self):
        tk.Label(self, text="🍦 Catálogo de Sabores Visual", font=FONT_TITULO, 
                 bg=FONDO, fg=MORADO).pack(anchor="w", pady=(0, 10))

        # --- GALERÍA SUPERIOR ---
        galeria_frame = tk.LabelFrame(self, text=" Sabores en Vitrina ", font=("Arial", 10, "bold"),
                                     bg=FONDO, fg=MORADO, padx=10, pady=10)
        galeria_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.canvas = tk.Canvas(galeria_frame, bg=FONDO, highlightthickness=0)
        scrollbar = ttk.Scrollbar(galeria_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_content = tk.Frame(self.canvas, bg=FONDO)

        self.scrollable_content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- GESTIÓN INFERIOR ---
        gestion_f = tk.Frame(self, bg=FONDO)
        gestion_f.pack(fill="x", side="bottom", pady=15)

        tk.Label(gestion_f, text="📋 Consultar y Editar Sabores", font=("Arial", 11, "bold"), 
                 bg=FONDO, fg=TEXTO_OSCURO).pack(anchor="w", padx=20)

        cols = ("ID", "Sabor", "Categoría", "Precio")
        self.tabla = ttk.Treeview(gestion_f, columns=cols, show="headings", height=5)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, anchor="center", width=120)
        self.tabla.pack(fill="x", padx=20, pady=5)

        btns = tk.Frame(gestion_f, bg=FONDO)
        btns.pack(pady=5)
        self._crear_btn(btns, "➕ Nuevo", TURQUESA, self._abrir_crear).pack(side="left", padx=5)
        self._crear_btn(btns, "📝 Editar", MORADO, self._abrir_editar).pack(side="left", padx=5)
        # AQUÍ ES DONDE LLAMAMOS A LA FUNCIÓN QUE FALTABA
        self._crear_btn(btns, "🗑️ Desactivar", "#e74c3c", self._baja_logica).pack(side="left", padx=5)

        self.cargar_datos()

    def _crear_btn(self, parent, txt, col, cmd):
        return tk.Button(parent, text=txt, bg=col, fg=BLANCO, font=("Arial", 9, "bold"),
                         relief="flat", padx=15, pady=8, cursor="hand2", command=cmd)

    def cargar_datos(self):
        for w in self.scrollable_content.winfo_children(): w.destroy()
        for i in self.tabla.get_children(): self.tabla.delete(i)
        self.imagenes_refs = []

        sabores = self.dao.listar_activos()
        columnas_max = 4

        for i, s in enumerate(sabores):
            fila, col = i // columnas_max, i % columnas_max
            self._dibujar_tarjeta(s, fila, col)
            self.tabla.insert("", "end", values=(s.id_sabor, s.nombre, s.categoria, f"${s.precio_unitario:.2f}"))

    def _dibujar_tarjeta(self, sabor, f, c):
        card = tk.Frame(self.scrollable_content, bg=BLANCO, highlightthickness=1, 
                        highlightbackground=MORADO_MED, padx=10, pady=10)
        card.grid(row=f, column=c, padx=15, pady=15)

        # 1. Definimos la ruta base de tu carpeta de imágenes (Ruta Absoluta)
        # Nota: Ajusté la ruta según tu captura, quitando el 'src' si static está afuera
        CARPETA_IMAGENES = r"C:\Users\sansn\Documents\Lupita\LupitaSoft\src\static\images"
        
        # 2. Intentamos armar la ruta con el número de ID
        nombre_archivo = f"{sabor.id_sabor}.png"
        img_path = os.path.join(CARPETA_IMAGENES, nombre_archivo)
        
        # 3. Si NO existe la imagen con ese número, usamos la de default
        if not os.path.exists(img_path):
            img_path = os.path.join(CARPETA_IMAGENES, "default.png")
        try:
            # Abrir y redimensionar
            img = Image.open(img_path).resize((110, 110), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # CRITICAL: Guardar referencia para que no desaparezca
            self.imagenes_refs.append(photo)
            
            tk.Label(card, image=photo, bg=BLANCO).pack()
        except Exception as e:
            # Si falla la carga (archivo corrupto o no hay default), emoji de respaldo
            tk.Label(card, text="🍦", font=("Arial", 40), bg=BLANCO).pack()
            print(f"DEBUG: No se pudo cargar {img_path}: {e}")

        # Nombre y Precio
        tk.Label(card, text=sabor.nombre, font=("Arial", 10, "bold"), bg=BLANCO).pack(pady=5)
        tk.Label(card, text=f"${sabor.precio_unitario:.2f}", font=("Arial", 9), bg=BLANCO, fg=TURQUESA).pack()
    
    def _abrir_crear(self): self._ventana_form("crear")
    
    def _abrir_editar(self):
        sel = self.tabla.selection()
        if not sel: return messagebox.showwarning("Aviso", "Selecciona un sabor")
        self._ventana_form("editar", self.tabla.item(sel)['values'])

    def _ventana_form(self, modo, datos=None):
        v = tk.Toplevel(self)
        v.title("Gestión de Sabores")
        v.geometry("400x650")
        v.configure(bg=MORADO_CLARO)
        v.grab_set()

        tk.Label(v, text="🍨 DATOS DEL SABOR", font=("Georgia", 12, "bold"), bg=MORADO_CLARO).pack(pady=20)

        f = tk.Frame(v, bg=MORADO_CLARO); f.pack(padx=30)
        tk.Label(f, text="Nombre:", bg=MORADO_CLARO).pack(anchor="w")
        ent_nom = tk.Entry(f, width=35); ent_nom.pack(pady=5)
        
        tk.Label(f, text="Categoría:", bg=MORADO_CLARO).pack(anchor="w")
        cb_cat = ttk.Combobox(f, values=["Agua", "Leche", "Especial"], state="readonly", width=32)
        cb_cat.pack(pady=5); cb_cat.set("Leche")

        tk.Label(f, text="Precio:", bg=MORADO_CLARO).pack(anchor="w")
        ent_pre = tk.Entry(f, width=35); ent_pre.pack(pady=5)

        # SECCIÓN IMAGEN
        lbl_status = tk.Label(v, text="Sin imagen seleccionada", bg=MORADO_CLARO, fg=TEXTO_GRIS)
        lbl_status.pack()

        def seleccionar():
            ruta = filedialog.askopenfilename(filetypes=[("PNG", "*.png")])
            if ruta:
                self.ruta_nueva_img.set(ruta)
                lbl_status.config(text=os.path.basename(ruta), fg="green")

        tk.Button(v, text="📂 Elegir PNG", command=seleccionar).pack(pady=5)

        if modo == "editar":
            ent_nom.insert(0, datos[1]); cb_cat.set(datos[2])
            ent_pre.insert(0, str(datos[3]).replace('$', ''))

        def guardar():
            n, c, p = ent_nom.get(), cb_cat.get(), ent_pre.get()
            img_sel = self.ruta_nueva_img.get()
            
            if modo == "crear":
                sabor = self.dao.crear_sabor(n, c, float(p), "default.png")
                id_f = sabor.id_sabor
            else:
                id_f = datos[0]
                self.dao.actualizar_sabor(id_f, {'nombre':n, 'categoria':c, 'precio':float(p)})

            if img_sel:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                destino = os.path.join(BASE_DIR, "static", "images", f"{id_f}.png")
                shutil.copy(img_sel, destino)

            self.cargar_datos()
            v.destroy()

        tk.Button(v, text="💾 GUARDAR", bg=TURQUESA, fg=BLANCO, font=("Arial", 11, "bold"),
                  command=guardar, padx=30, pady=12).pack(pady=30)

    # --- LA FUNCIÓN QUE FALTABA ---
    def _baja_logica(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un sabor de la tabla.")
            return
        
        id_sabor = self.tabla.item(seleccion)['values'][0]
        nombre = self.tabla.item(seleccion)['values'][1]

        if messagebox.askyesno("Confirmar", f"¿Deseas desactivar el sabor '{nombre}'?"):
            if self.dao.desactivar_sabor(id_sabor):
                messagebox.showinfo("Éxito", "Sabor desactivado correctamente.")
                self.cargar_datos()