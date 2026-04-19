import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import urllib.request
import io

# PARCHE DE RUTA: Asegura que Python encuentre la carpeta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importación de constantes y todas las vistas
from src.ui.constants import *
from src.ui.login_view import LoginView
from src.ui.sidebar_view import SidebarView
from src.ui.dashboard_view import DashboardView
from src.ui.inventario_view import InventarioView
from src.ui.ventas_view import VentasView
from src.ui.sabor_view import SaborView
from src.ui.receta_view import RecetaView
from src.ui.usuario_view import UsuarioView


class LupitaSoftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la Ventana Principal
        self.title("LupitaSoft — Heladería Lupita")
        self.geometry("1150x700")
        self.configure(bg=FONDO)
        
        # Variables de sesión
        self.usuario_id = None
        self.rol = None
        self.frame_actual = None
        
        # Cargar Logo desde tu URL original
        self.logo_img = self._cargar_logo()
        
        # Arrancar con el Login
        self.mostrar_login()

    def _cargar_logo(self):
        """Carga el logo oficial desde la web como en tu diseño original"""
        try:
            url = "https://media.base44.com/images/public/69e1a68f901a409e0d030b63/f5ef7e54d_image.png"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as r:
                img_data = r.read()
                img = Image.open(io.BytesIO(img_data)).resize((90, 90), Image.LANCZOS)
                return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error cargando logo: {e}")
            return None

    def mostrar_login(self):
        """Limpia la ventana y muestra la pantalla de acceso"""
        if self.frame_actual: 
            self.frame_actual.destroy()
        
        # Le pasamos el logo cargado para que se vea en el login
        self.frame_actual = LoginView(self, self.entrar_al_sistema, self.logo_img)
        self.frame_actual.pack(fill="both", expand=True)

    def entrar_al_sistema(self, rol, usuario_id):
        """Layout principal: Sidebar + Borde 2px + Topbar + Contenido"""
        self.rol = rol
        self.usuario_id = usuario_id
        
        # Limpiar el login
        self.frame_actual.destroy()

        # 1. SIDEBAR (Tu diseño original)
        self.sidebar = SidebarView(self, self.cambiar_seccion, self.rol, self.logo_img)
        self.sidebar.pack(side="left", fill="y")
        
        # 2. BORDE TURQUESA DE 2PX (Tu toque distintivo)
        tk.Frame(self, bg=TURQUESA_MED, width=2).pack(side="left", fill="y")

        # 3. CONTENEDOR DERECHO
        self.contenedor = tk.Frame(self, bg=FONDO)
        self.contenedor.pack(side="left", fill="both", expand=True)

        # 4. TOPBAR (Tu diseño original con el lema)
        self.topbar = tk.Frame(self.contenedor, bg=BLANCO, height=54)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        
        self.titulo_var = tk.StringVar(value="Dashboard")
        tk.Label(self.topbar, textvariable=self.titulo_var, font=FONT_TITULO,
                 bg=BLANCO, fg=MORADO).pack(side="left", padx=22, pady=14)
        
        tk.Label(self.topbar, text="Est. 1979  •  Sabor • Pasión • Tradición",
                 font=("Arial", 9), bg=BLANCO, fg=TEXTO_GRIS).pack(side="right", padx=18)
        
        # Línea divisoria del Topbar
        tk.Frame(self.contenedor, bg=TURQUESA_MED, height=2).pack(fill="x")

        # 5. VISTA ACTIVA (Donde se cargan las pantallas)
        self.vista_activa = tk.Frame(self.contenedor, bg=FONDO)
        self.vista_activa.pack(fill="both", expand=True, padx=22, pady=14)
        
        # Iniciar en el Dashboard
        self.cambiar_seccion("dashboard")

    def cambiar_seccion(self, seccion):
        """
        Controlador de navegación: Limpia el área de contenido y 
        despliega la vista seleccionada con sus parámetros correctos.
        """
        # 1. Limpiar lo que haya en la vista actual
        for w in self.vista_activa.winfo_children(): 
            w.destroy()

        # 2. Diccionario de Títulos (Para actualizar el Topbar de tu diseño original)
        titulos = {
            "dashboard": "📊  Dashboard Principal",
            "inventario": "📦  Control de Inventario",
            "ventas": "💰  Punto de Venta",
            "sabores": "🍦  Catálogo de los 72 Sabores",
            "recetas": "👨‍🍳  Panel de Producción (Cocina)",
            "usuarios": "👥  Gestión de Personal y Accesos",
            "pedidos": "🛒  Logística de Pedidos (Eventos)"
        }

        # Actualizar el título en el Topbar
        self.titulo_var.set(titulos.get(seccion, "LupitaSoft"))

        # 3. Lógica de Carga de Vistas
        try:
            if seccion == "dashboard":
                DashboardView(self.vista_activa).pack(fill="both", expand=True)

            elif seccion == "inventario":
                InventarioView(self.vista_activa).pack(fill="both", expand=True)

            elif seccion == "ventas":
                # Esta vista es especial: requiere tu id_usuario para la bitácora
                VentasView(self.vista_activa, self.usuario_id).pack(fill="both", expand=True)

            elif seccion == "sabores":
                SaborView(self.vista_activa).pack(fill="both", expand=True)

            elif seccion == "recetas":
                # Recuerda: Esta vista pedirá el código 'LUPITA1979' al iniciar
                RecetaView(self.vista_activa).pack(fill="both", expand=True)

            elif seccion == "usuarios":
                # Solo accesible si eres Admin (HLA01)
                UsuarioView(self.vista_activa).pack(fill="both", expand=True)

            elif seccion == "pedidos":
                # La nueva vista de logística para eventos que pediste
                from src.ui.pedidos_view import PedidosView
                PedidosView(self.vista_activa).pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar la sección {seccion}.\nDetalle: {e}")
if __name__ == "__main__":
    app = LupitaSoftApp()
    app.mainloop()