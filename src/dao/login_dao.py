from src.database.db_config import SessionLocal
from src.models.usuario import Usuario

class LoginDAO:
    def __init__(self):
        self.db = SessionLocal()

    def autenticar(self, correo_codigo, password):
        # Busca al usuario por su código de identificación
        user = self.db.query(Usuario).filter(Usuario.correo == correo_codigo).first()
        if user and user.contrasena == password:
            return {"valido": True, "rol": user.rol, "id": user.id_usuario}
        return {"valido": False}