import tkinter as tk
from src.ui.constants import *

class SidebarView(tk.Frame):
    def __init__(self, parent, cambiar_pantalla, rol, logo_img):
        # Ahora acepta 4 argumentos + self = 5 (Igual que en main.py)
        super().__init__(parent, bg=SIDEBAR_BG, width=220)
        self.cambiar_pantalla = cambiar_pantalla
        self.rol = rol
        self.logo_img = logo_img
        self.pack_propagate(False)
        self._init_ui()

    def _init_ui(self):
        # 1. LOGO: Si hay logo cargado, lo usamos. Si no, usamos el emoji 🍦
        if self.logo_img:
            tk.Label(self, image=self.logo_img, bg=SIDEBAR_BG).pack(pady=(20, 5))
        else:
            tk.Label(self, text="🍧", font=("Arial", 45), bg=SIDEBAR_BG, fg=TURQUESA).pack(pady=(20, 5))
            
        tk.Label(self, text="LupitaSoft", font=("Georgia", 14, "bold italic"), 
                 bg=SIDEBAR_BG, fg=MORADO).pack()
        
        # Línea divisoria (Borde de 1px usando tu MORADO_MED)
        tk.Frame(self, bg=MORADO_MED, height=1).pack(fill="x", padx=20, pady=15)

        # 2. SECCIONES GENERALES
        self._crear_btn("  Dashboard", "dashboard")
        self._crear_btn("  Inventario", "inventario")
        self._crear_btn("  Ventas", "ventas")
        self._crear_btn(" Catálogo", "sabores")
        # 3. SECCIONES DE GERENCIA (Solo para Admin / HLA01)
        if self.rol == "Admin":
            tk.Label(self, text="GERENCIA", font=("Arial", 7, "bold"), 
                     bg=SIDEBAR_BG, fg=TEXTO_GRIS).pack(anchor="w", padx=20, pady=(15, 0))
            self._crear_btn("  Usuarios", "usuarios")
            # El de reportes lo dejamos como texto por ahora si no tienes la vista
            self._crear_btn("  Reportes", "reportes")

        # 4. SECCIÓN COCINA
        tk.Label(self, text="PRODUCCIÓN", font=("Arial", 7, "bold"), 
                 bg=SIDEBAR_BG, fg=TEXTO_GRIS).pack(anchor="w", padx=20, pady=(15, 0))
        self._crear_btn("  Vista Cocinero", "recetas")
        self._crear_btn("  Pedidos Eventos", "pedidos")
    def _crear_btn(self, texto, comando):
        """Crea botones con el estilo lila de tu diseño original"""
        btn = tk.Button(self, text=texto, bg=SIDEBAR_BTN, fg=TEXTO_OSCURO,
                        font=("Arial", 10), relief="flat", cursor="hand2",
                        anchor="w", padx=15, pady=10,
                        activebackground=TURQUESA_MED,
                        command=lambda: self.cambiar_pantalla(comando))
        btn.pack(fill="x", padx=10, pady=2)