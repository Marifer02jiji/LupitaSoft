import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import urllib.request
import io

# ============================================================
#  COLORES PASTEL — basados en el logo Lupita Helados
# ============================================================
TURQUESA        = "#4ecdc4"   # turquesa pastel principal
TURQUESA_CLARO  = "#e8f8f7"   # fondo turquesa muy suave
TURQUESA_MED    = "#a8e6e2"   # turquesa medio
MORADO          = "#9b72cf"   # morado pastel
MORADO_CLARO    = "#f0eaf9"   # fondo morado suave
MORADO_MED      = "#c9a8e8"   # morado medio
ROSA_PASTEL     = "#f0a8d0"   # acento rosa
AMARILLO_PASTEL = "#fff9c4"   # acento amarillo suave
BLANCO          = "#ffffff"
FONDO           = "#f7fffe"   # casi blanco turquesa
TEXTO_OSCURO    = "#2d2d4e"   # morado muy oscuro para texto
TEXTO_GRIS      = "#8892a4"
SIDEBAR_BG      = "#f0eaf9"   # sidebar morado muy claro
SIDEBAR_BTN     = "#e0d0f5"

# ============================================================
#  DATOS EN MEMORIA
# ============================================================
inventario = [
    {"nombre": "Leche entera",   "categoria": "leche",        "cantidad": 20, "unidad": "L",    "stock_min": 10, "caducidad": "2026-04-25"},
    {"nombre": "Fresa",          "categoria": "frutas",       "cantidad": 3,  "unidad": "kg",   "stock_min": 5,  "caducidad": "2026-04-20"},
    {"nombre": "Vainilla",       "categoria": "saborizantes", "cantidad": 8,  "unidad": "pzas", "stock_min": 3,  "caducidad": "2026-12-01"},
]
ventas = []
pedidos = []
sabores = [
    {"nombre": "Fresa",      "precio": 15.0, "activo": True},
    {"nombre": "Vainilla",   "precio": 15.0, "activo": True},
    {"nombre": "Chocolate",  "precio": 18.0, "activo": True},
    {"nombre": "Mango",      "precio": 17.0, "activo": True},
]
recetas = [
    {"nombre": "Helado de Fresa",     "sabor": "Fresa",     "rendimiento": "5 L", "tiempo": "45 min"},
    {"nombre": "Helado de Vainilla",  "sabor": "Vainilla",  "rendimiento": "5 L", "tiempo": "30 min"},
]
usuarios = [
    {"nombre": "Administrador",  "rol": "admin",    "email": "admin@lupita.com"},
    {"nombre": "Chef Lupita",    "rol": "cocinero", "email": "cocina@lupita.com"},
]

# ============================================================
#  VENTANA PRINCIPAL
# ============================================================
root = tk.Tk()
root.title("LupitaSoft — Heladería Lupita")
root.geometry("1100x660")
root.configure(bg=FONDO)
root.resizable(True, True)

# ============================================================
#  CARGAR LOGO DESDE URL
# ============================================================
logo_img = None
try:
    url = "https://media.base44.com/images/public/69e1a68f901a409e0d030b63/f5ef7e54d_image.png"
    with urllib.request.urlopen(url) as r:
        data = r.read()
    img = Image.open(io.BytesIO(data)).resize((90, 90), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(img)
except Exception:
    logo_img = None

# ============================================================
#  SIDEBAR
# ============================================================
sidebar = tk.Frame(root, bg=SIDEBAR_BG, width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# Borde derecho decorativo
tk.Frame(root, bg=TURQUESA_MED, width=2).pack(side="left", fill="y")

# Logo en sidebar
if logo_img:
    tk.Label(sidebar, image=logo_img, bg=SIDEBAR_BG).pack(pady=(16, 2))
else:
    tk.Label(sidebar, text="🍦", font=("Arial", 40), bg=SIDEBAR_BG, fg=TURQUESA).pack(pady=(16, 2))

tk.Label(sidebar, text="LupitaSoft", font=("Georgia", 13, "bold italic"),
         bg=SIDEBAR_BG, fg=MORADO).pack()
tk.Label(sidebar, text="Sistema de Gestión", font=("Arial", 8),
         bg=SIDEBAR_BG, fg=TEXTO_GRIS).pack(pady=(0, 10))

# Separador
tk.Frame(sidebar, bg=MORADO_MED, height=1).pack(fill="x", padx=16, pady=4)

# ============================================================
#  ÁREA DE CONTENIDO
# ============================================================
contenido = tk.Frame(root, bg=FONDO)
contenido.pack(side="left", fill="both", expand=True)

# Topbar
topbar = tk.Frame(contenido, bg=BLANCO, height=54)
topbar.pack(fill="x")
topbar.pack_propagate(False)
titulo_var = tk.StringVar(value="Dashboard")
tk.Label(topbar, textvariable=titulo_var, font=("Georgia", 15, "bold italic"),
         bg=BLANCO, fg=MORADO).pack(side="left", padx=22, pady=14)
tk.Label(topbar, text="Est. 1979  •  Sabor • Pasión • Tradición",
         font=("Arial", 9), bg=BLANCO, fg=TEXTO_GRIS).pack(side="right", padx=18)
tk.Frame(contenido, bg=TURQUESA_MED, height=2).pack(fill="x")

frame_actual = [None]

def mostrar_frame(frame):
    if frame_actual[0]:
        frame_actual[0].destroy()
    frame_actual[0] = frame
    frame.pack(fill="both", expand=True, padx=22, pady=14)

# ============================================================
#  ESTILOS TABLA
# ============================================================
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
    background=BLANCO, foreground=TEXTO_OSCURO,
    rowheight=28, fieldbackground=BLANCO,
    font=("Arial", 10))
style.configure("Treeview.Heading",
    background=TURQUESA, foreground=BLANCO,
    font=("Arial", 10, "bold"), relief="flat")
style.map("Treeview", background=[("selected", TURQUESA_CLARO)])

def boton_accion(parent, texto, cmd, color=TURQUESA):
    return tk.Button(parent, text=texto, command=cmd,
                     bg=color, fg=BLANCO, font=("Arial", 10, "bold"),
                     relief="flat", cursor="hand2", padx=12, pady=6,
                     activebackground=MORADO, activeforeground=BLANCO)

def label_seccion(parent, texto):
    tk.Label(parent, text=texto, font=("Georgia", 12, "bold italic"),
             bg=FONDO, fg=MORADO).pack(anchor="w", pady=(0, 6))

# ============================================================
#  PANTALLA: DASHBOARD
# ============================================================
def pantalla_dashboard():
    titulo_var.set("📊  Dashboard")
    f = tk.Frame(contenido, bg=FONDO)

    total_ventas = sum(v["total"] for v in ventas)
    bajo_stock   = sum(1 for i in inventario if i["cantidad"] <= i["stock_min"])
    pedidos_pend = sum(1 for p in pedidos if p.get("estatus") == "pendiente")

    tarjetas = [
        ("💰 Ventas hoy",      f"${total_ventas:.2f}", TURQUESA,  TURQUESA_CLARO),
        ("📦 Bajo stock",      str(bajo_stock),         "#e8a87c", "#fff3e8"),
        ("🛒 Pedidos pend.",   str(pedidos_pend),       MORADO,    MORADO_CLARO),
        ("🍦 Sabores activos", str(sum(1 for s in sabores if s["activo"])), "#a8d8a8", "#edf7ed"),
    ]

    row = tk.Frame(f, bg=FONDO)
    row.pack(pady=16)
    for titulo, valor, color, fondo in tarjetas:
        card = tk.Frame(row, bg=fondo, width=188, height=108,
                        highlightbackground=color, highlightthickness=2)
        card.pack(side="left", padx=10)
        card.pack_propagate(False)
        tk.Label(card, text=titulo, bg=fondo, fg=color,
                 font=("Arial", 9, "bold")).pack(pady=(18, 2))
        tk.Label(card, text=valor,  bg=fondo, fg=color,
                 font=("Arial", 26, "bold")).pack()

    # Bienvenida
    wel = tk.Frame(f, bg=BLANCO, highlightbackground=TURQUESA_MED, highlightthickness=1)
    wel.pack(fill="x", pady=8)
    tk.Label(wel, text="¡Bienvenido al sistema LupitaSoft! 🍦\nSabor • Pasión • Tradición • Excelencia   Est. 1979",
             bg=BLANCO, fg=TEXTO_GRIS, font=("Georgia", 11, "italic"), justify="center").pack(pady=18)

    mostrar_frame(f)

# ============================================================
#  PANTALLA: INVENTARIO
# ============================================================
def pantalla_inventario():
    titulo_var.set("📦  Inventario")
    f = tk.Frame(contenido, bg=FONDO)
    label_seccion(f, "Control de Insumos")

    cols = ("Nombre", "Categoría", "Cantidad", "Unidad", "Mín.", "Caducidad", "Estado")
    tabla = ttk.Treeview(f, columns=cols, show="headings", height=10)
    for c in cols:
        tabla.heading(c, text=c)
        tabla.column(c, width=118, anchor="center")
    tabla.tag_configure("rojo",    background="#fde8e8", foreground="#c0392b")
    tabla.tag_configure("amarillo",background="#fef9e7", foreground="#d35400")
    tabla.tag_configure("verde",   background="#e8fdf0", foreground="#1a7a4a")

    def cargar():
        tabla.delete(*tabla.get_children())
        for item in inventario:
            if item["cantidad"] <= 0:
                estado, tag = "🔴 Agotado", "rojo"
            elif item["cantidad"] <= item["stock_min"]:
                estado, tag = "🟡 Bajo stock", "amarillo"
            else:
                estado, tag = "🟢 OK", "verde"
            tabla.insert("", "end", values=(
                item["nombre"], item["categoria"], item["cantidad"],
                item["unidad"], item["stock_min"], item["caducidad"], estado
            ), tags=(tag,))
    cargar()
    tabla.pack(fill="both", expand=True)

    form_f = tk.Frame(f, bg=TURQUESA_CLARO, highlightbackground=TURQUESA_MED, highlightthickness=1)
    form_f.pack(fill="x", pady=8)
    form = tk.Frame(form_f, bg=TURQUESA_CLARO)
    form.pack(pady=8)
    campos = ["Nombre","Categoría","Cantidad","Unidad","Stock mín.","Caducidad (YYYY-MM-DD)"]
    entradas = []
    for i, c in enumerate(campos):
        tk.Label(form, text=c, bg=TURQUESA_CLARO, fg=TEXTO_OSCURO,
                 font=("Arial", 8, "bold")).grid(row=0, column=i, padx=4)
        e = tk.Entry(form, width=13, relief="flat",
                     highlightbackground=TURQUESA, highlightthickness=1)
        e.grid(row=1, column=i, padx=4)
        entradas.append(e)

    def agregar():
        try:
            inventario.append({
                "nombre": entradas[0].get(), "categoria": entradas[1].get(),
                "cantidad": float(entradas[2].get()), "unidad": entradas[3].get(),
                "stock_min": float(entradas[4].get()), "caducidad": entradas[5].get(),
            })
            for e in entradas: e.delete(0, "end")
            cargar()
        except ValueError:
            messagebox.showerror("Error", "Cantidad y Stock mínimo deben ser números.")

    boton_accion(form, "➕ Agregar", agregar).grid(row=1, column=len(campos), padx=10)
    mostrar_frame(f)

# ============================================================
#  PANTALLA: VENTAS
# ============================================================
def pantalla_ventas():
    titulo_var.set("💰  Ventas")
    f = tk.Frame(contenido, bg=FONDO)
    label_seccion(f, "Registro de Ventas")

    cols = ("Sabor", "Cantidad", "Precio unit.", "Total", "Tipo", "Fecha")
    tabla = ttk.Treeview(f, columns=cols, show="headings", height=9)
    for c in cols:
        tabla.heading(c, text=c)
        tabla.column(c, width=140, anchor="center")

    def cargar():
        tabla.delete(*tabla.get_children())
        for v in ventas:
            tabla.insert("", "end", values=(
                v["sabor"], v["cantidad"], f"${v['precio']:.2f}",
                f"${v['total']:.2f}", v.get("tipo","mostrador"), v["fecha"]
            ))
    cargar()
    tabla.pack(fill="both", expand=True)

    form_f = tk.Frame(f, bg=MORADO_CLARO, highlightbackground=MORADO_MED, highlightthickness=1)
    form_f.pack(fill="x", pady=8)
    form = tk.Frame(form_f, bg=MORADO_CLARO)
    form.pack(pady=8)
    labels = ["Sabor","Cantidad","Precio unitario","Tipo","Fecha (YYYY-MM-DD)"]
    entradas = []
    for i, l in enumerate(labels):
        tk.Label(form, text=l, bg=MORADO_CLARO, fg=TEXTO_OSCURO,
                 font=("Arial", 8, "bold")).grid(row=0, column=i, padx=4)
        e = tk.Entry(form, width=15, relief="flat",
                     highlightbackground=MORADO, highlightthickness=1)
        e.grid(row=1, column=i, padx=4)
        entradas.append(e)

    def registrar():
        try:
            cant = float(entradas[1].get())
            precio = float(entradas[2].get())
            ventas.append({
                "sabor": entradas[0].get(), "cantidad": cant,
                "precio": precio, "total": cant * precio,
                "tipo": entradas[3].get(), "fecha": entradas[4].get()
            })
            for e in entradas: e.delete(0, "end")
            cargar()
        except ValueError:
            messagebox.showerror("Error", "Cantidad y Precio deben ser números.")

    boton_accion(form, "✔ Registrar", registrar, MORADO).grid(row=1, column=len(labels), padx=10)
    mostrar_frame(f)

# ============================================================
#  PANTALLA: PEDIDOS
# ============================================================
def pantalla_pedidos():
    titulo_var.set("🛒  Pedidos")
    f = tk.Frame(contenido, bg=FONDO)
    label_seccion(f, "Gestión de Pedidos")

    cols = ("Cliente","Teléfono","Sabores","Total","Anticipo","Entrega","Estatus")
    tabla = ttk.Treeview(f, columns=cols, show="headings", height=9)
    for c in cols:
        tabla.heading(c, text=c)
        tabla.column(c, width=130, anchor="center")

    for p in pedidos:
        tabla.insert("", "end", values=(
            p.get("cliente",""), p.get("telefono",""), p.get("sabores",""),
            f"${p.get('total',0):.2f}", f"${p.get('anticipo',0):.2f}",
            p.get("entrega",""), p.get("estatus","pendiente")
        ))
    tabla.pack(fill="both", expand=True)

    info = tk.Label(f, text="⚙️  Módulo en desarrollo — pronto podrás crear, editar y dar seguimiento a pedidos.",
                    bg=AMARILLO_PASTEL, fg=TEXTO_OSCURO, font=("Arial", 10), pady=10)
    info.pack(fill="x", pady=8)
    mostrar_frame(f)

# ============================================================
#  PANTALLA: SABORES
# ============================================================
def pantalla_sabores():
    titulo_var.set("🍦  Sabores")
    f = tk.Frame(contenido, bg=FONDO)
    label_seccion(f, "Catálogo de Sabores")

    cols = ("Nombre","Precio por bola","Disponible")
    tabla = ttk.Treeview(f, columns=cols, show="headings", height=10)
    for c in cols:
        tabla.heading(c, text=c)
        tabla.column(c, width=220, anchor="center")
    for s in sabores:
        tabla.insert("", "end", values=(
            s["nombre"], f"${s['precio']:.2f}", "✅ Sí" if s["activo"] else "❌ No"
        ))
    tabla.pack(fill="both", expand=True)

    info = tk.Label(f, text="⚙️  Módulo en desarrollo — pronto podrás agregar, editar y desactivar sabores.",
                    bg=AMARILLO_PASTEL, fg=TEXTO_OSCURO, font=("Arial", 10), pady=10)
    info.pack(fill="x", pady=8)
    mostrar_frame(f)

# ============================================================
#  PANTALLA: RECETAS
# ============================================================
def pantalla_recetas():
    titulo_var.set("📖  Recetas")
    f = tk.Frame(contenido, bg=FONDO)
    label_seccion(f, "Libro de Recetas")

    cols = ("Nombre de receta","Sabor","Rendimiento","Tiempo prep.")
    tabla = ttk.Treeview(f, columns=cols, show="headings", height=10)
    for c in cols:
        tabla.heading(c, text=c)
        tabla.column(c, width=200, anchor="center")
    for r in recetas:
        tabla.insert("", "end", values=(
            r["nombre"], r["sabor"], r["rendimiento"], r["tiempo"]
        ))
    tabla.pack(fill="both", expand=True)

    info = tk.Label(f, text="⚙️  Módulo en desarrollo — pronto podrás gestionar recetas con ingredientes y pasos.",
                    bg=AMARILLO_PASTEL, fg=TEXTO_OSCURO, font=("Arial", 10), pady=10)
    info.pack(fill="x", pady=8)
    mostrar_frame(f)

# ============================================================
#  PANTALLA: USUARIOS
# ============================================================
def pantalla_usuarios():
    titulo_var.set("👥  Usuarios")
    f = tk.Frame(contenido, bg=FONDO)
    label_seccion(f, "Gestión de Usuarios")

    cols = ("Nombre","Rol","Correo")
    tabla = ttk.Treeview(f, columns=cols, show="headings", height=10)
    for c in cols:
        tabla.heading(c, text=c)
        tabla.column(c, width=260, anchor="center")
    tabla.tag_configure("admin",    background="#f0eaf9", foreground=MORADO)
    tabla.tag_configure("cocinero", background="#e8f8f7", foreground="#1a7a4a")
    for u in usuarios:
        tabla.insert("", "end", values=(u["nombre"], u["rol"].capitalize(), u["email"]),
                     tags=(u["rol"],))
    tabla.pack(fill="both", expand=True)

    info = tk.Label(f, text="⚙️  Módulo en desarrollo — pronto podrás invitar y gestionar accesos.",
                    bg=AMARILLO_PASTEL, fg=TEXTO_OSCURO, font=("Arial", 10), pady=10)
    info.pack(fill="x", pady=8)
    mostrar_frame(f)

# ============================================================
#  PANTALLA: REPORTES
# ============================================================
def pantalla_reportes():
    titulo_var.set("📊  Reportes")
    f = tk.Frame(contenido, bg=FONDO)
    label_seccion(f, "Reportes y Estadísticas")

    reportes = [
        ("📈 Ventas por día",          "Próximamente"),
        ("🍦 Sabores más vendidos",     "Próximamente"),
        ("📦 Historial de inventario",  "Próximamente"),
        ("💰 Ingresos mensuales",       "Próximamente"),
        ("🛒 Pedidos completados",      "Próximamente"),
    ]
    for nombre, estado in reportes:
        fila = tk.Frame(f, bg=BLANCO, highlightbackground=TURQUESA_MED, highlightthickness=1)
        fila.pack(fill="x", pady=4)
        tk.Label(fila, text=nombre, bg=BLANCO, fg=TEXTO_OSCURO,
                 font=("Arial", 11), width=35, anchor="w").pack(side="left", padx=16, pady=10)
        tk.Label(fila, text=estado, bg=BLANCO, fg=TEXTO_GRIS,
                 font=("Arial", 9, "italic")).pack(side="right", padx=16)

    mostrar_frame(f)

# ============================================================
#  PANTALLA: VISTA COCINERO
# ============================================================
def pantalla_cocinero():
    titulo_var.set("👨‍🍳  Vista Cocinero")
    f = tk.Frame(contenido, bg=FONDO)

    # Encabezado cocinero
    enc = tk.Frame(f, bg=TURQUESA_CLARO, highlightbackground=TURQUESA, highlightthickness=1)
    enc.pack(fill="x", pady=(0,12))
    tk.Label(enc, text="👨‍🍳  Panel del Cocinero", font=("Georgia", 13, "bold italic"),
             bg=TURQUESA_CLARO, fg=TURQUESA).pack(side="left", padx=16, pady=12)
    tk.Label(enc, text="Solo lectura — acceso con código de cocina",
             font=("Arial", 9), bg=TURQUESA_CLARO, fg=TEXTO_GRIS).pack(side="right", padx=16)

    # Recetas del día
    tk.Label(f, text="📖  Recetas disponibles", font=("Georgia", 11, "bold italic"),
             bg=FONDO, fg=MORADO).pack(anchor="w", pady=(0,4))
    cols_r = ("Receta","Sabor","Rendimiento","Tiempo")
    tr = ttk.Treeview(f, columns=cols_r, show="headings", height=4)
    for c in cols_r:
        tr.heading(c, text=c)
        tr.column(c, width=200, anchor="center")
    for r in recetas:
        tr.insert("", "end", values=(r["nombre"], r["sabor"], r["rendimiento"], r["tiempo"]))
    tr.pack(fill="x", pady=(0,12))

    # Inventario (solo lectura)
    tk.Label(f, text="📦  Estado del inventario", font=("Georgia", 11, "bold italic"),
             bg=FONDO, fg=MORADO).pack(anchor="w", pady=(0,4))
    cols_i = ("Insumo","Cantidad","Unidad","Estado")
    ti = ttk.Treeview(f, columns=cols_i, show="headings", height=5)
    for c in cols_i:
        ti.heading(c, text=c)
        ti.column(c, width=200, anchor="center")
    ti.tag_configure("rojo",    background="#fde8e8", foreground="#c0392b")
    ti.tag_configure("amarillo",background="#fef9e7", foreground="#d35400")
    ti.tag_configure("verde",   background="#e8fdf0", foreground="#1a7a4a")
    for item in inventario:
        if item["cantidad"] <= 0:
            estado, tag = "🔴 Agotado", "rojo"
        elif item["cantidad"] <= item["stock_min"]:
            estado, tag = "🟡 Bajo stock", "amarillo"
        else:
            estado, tag = "🟢 OK", "verde"
        ti.insert("", "end", values=(
            item["nombre"], item["cantidad"], item["unidad"], estado
        ), tags=(tag,))
    ti.pack(fill="x")

    info = tk.Label(f, text="⚙️  Próximamente: actualizar estatus de producción y solicitar insumos.",
                    bg=AMARILLO_PASTEL, fg=TEXTO_OSCURO, font=("Arial", 10), pady=10)
    info.pack(fill="x", pady=10)
    mostrar_frame(f)

# ============================================================
#  SEPARADORES Y SECCIONES SIDEBAR
# ============================================================
def sep_sidebar(texto):
    tk.Label(sidebar, text=texto, font=("Arial", 7, "bold"),
             bg=SIDEBAR_BG, fg=TEXTO_GRIS).pack(anchor="w", padx=14, pady=(10,1))
    tk.Frame(sidebar, bg=MORADO_MED, height=1).pack(fill="x", padx=14, pady=(0,2))

# ============================================================
#  BOTONES SIDEBAR
# ============================================================
btn_activo = [None]

def hacer_boton(texto, cmd):
    btn = tk.Button(sidebar, text=texto,
                    command=lambda b=None: [seleccionar(btn), cmd()],
                    bg=SIDEBAR_BTN, fg=TEXTO_OSCURO, font=("Arial", 10),
                    relief="flat", cursor="hand2",
                    activebackground=TURQUESA_MED, activeforeground=TEXTO_OSCURO,
                    width=22, pady=7, anchor="w", padx=10)
    btn.pack(fill="x", padx=8, pady=1)
    return btn

def seleccionar(btn):
    if btn_activo[0]:
        btn_activo[0].configure(bg=SIDEBAR_BTN, fg=TEXTO_OSCURO)
    btn.configure(bg=TURQUESA, fg=BLANCO)
    btn_activo[0] = btn

sep_sidebar("ADMINISTRACIÓN")
hacer_boton("  📊  Dashboard",    pantalla_dashboard)
hacer_boton("  📦  Inventario",   pantalla_inventario)
hacer_boton("  💰  Ventas",       pantalla_ventas)
hacer_boton("  🛒  Pedidos",      pantalla_pedidos)
hacer_boton("  🍦  Sabores",      pantalla_sabores)
hacer_boton("  📖  Recetas",      pantalla_recetas)
hacer_boton("  📊  Reportes",     pantalla_reportes)
hacer_boton("  👥  Usuarios",     pantalla_usuarios)

sep_sidebar("COCINA")
hacer_boton("  👨‍🍳  Vista Cocinero", pantalla_cocinero)

# Footer
tk.Frame(sidebar, bg=TURQUESA_MED, height=1).pack(fill="x", padx=14, side="bottom", pady=6)
tk.Label(sidebar, text="v1.0  •  Est. 1979", font=("Georgia", 8, "italic"),
         bg=SIDEBAR_BG, fg=TEXTO_GRIS).pack(side="bottom", pady=4)

# Instalar Pillow si no está
try:
    from PIL import Image
except ImportError:
    messagebox.showwarning("Dependencia",
        "Instala Pillow para ver el logo:\n\npip install Pillow\n\nLuego reinicia la app.")

pantalla_dashboard()
root.mainloop()