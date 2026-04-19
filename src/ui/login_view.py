import tkinter as tk
from tkinter import messagebox
from src.ui.constants import *
from src.dao.login_dao import LoginDAO

class LoginView(tk.Frame):
    def __init__(self, parent, al_loguear, logo_img):
        # Ahora acepta 3 argumentos + self = 4 (Igual que en main.py)
        super().__init__(parent, bg=FONDO)
        self.al_loguear = al_loguear
        self.logo_img = logo_img
        self.dao = LoginDAO()
        self._init_ui()

    def _init_ui(self):
        # Contenedor central (Tu diseño original)
        centro = tk.Frame(self, bg=BLANCO, padx=40, pady=40, 
                          highlightbackground=TURQUESA_MED, highlightthickness=2)
        centro.place(relx=0.5, rely=0.5, anchor="center")

        # Mostrar el logo si cargó correctamente
        if self.logo_img:
            tk.Label(centro, image=self.logo_img, bg=BLANCO).pack(pady=(0, 10))

        tk.Label(centro, text="🍦 LupitaSoft", font=("Georgia", 22, "bold italic"), 
                 bg=BLANCO, fg=MORADO).pack(pady=(0, 20))

        # Campos de entrada
        tk.Label(centro, text="Código de Usuario", bg=BLANCO, fg=TEXTO_OSCURO, font=("Arial", 10, "bold")).pack(anchor="w")
        self.ent_user = tk.Entry(centro, width=30, relief="flat", highlightthickness=1, highlightbackground=TURQUESA_MED)
        self.ent_user.pack(pady=(5, 15))

        tk.Label(centro, text="Contraseña", bg=BLANCO, fg=TEXTO_OSCURO, font=("Arial", 10, "bold")).pack(anchor="w")
        self.ent_pass = tk.Entry(centro, width=30, show="*", relief="flat", highlightthickness=1, highlightbackground=TURQUESA_MED)
        self.ent_pass.pack(pady=(5, 25))

        # Botón con tu estilo original
        tk.Button(centro, text="ENTRAR AL SISTEMA", command=self._intentar_login, 
                  bg=TURQUESA, fg=BLANCO, font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2", padx=30, pady=10).pack()

    def _intentar_login(self):
        user = self.ent_user.get()
        pw = self.ent_pass.get()
        res = self.dao.autenticar(user, pw)
        
        if res["valido"]:
            self.al_loguear(res["rol"], res["id"])
        else:
            messagebox.showerror("Error de Acceso", "Código o contraseña incorrectos.")