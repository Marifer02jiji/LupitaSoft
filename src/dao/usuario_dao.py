from src.database.db_config import SessionLocal
from src.models.usuario import Usuario
from src.models.empleado import Empleado

class UsuarioDAO:
    def __init__(self):
        self.db = SessionLocal()

    def listar_usuarios_completo(self):
        try:
            return self.db.query(Usuario, Empleado).join(
                Empleado, Usuario.id_empleado == Empleado.id_empleado
            ).all()
        except Exception as e:
            print(f"Error en UsuarioDAO: {e}")
            return []
        finally:
            SessionLocal.remove()
    
    def cambiar_rol(self, id_usuario, nuevo_rol):
        user = self.db.query(Usuario).get(id_usuario)
        if user:
            user.rol = nuevo_rol
            self.db.commit()
            return True
        return False
    
    def crear_usuario(self, correo, password, rol, id_emp):
        try:
            nuevo = Usuario(correo=correo, password=password, rol=rol, id_empleado=id_emp)
            self.db.add(nuevo)
            self.db.commit()
            return True
        except: 
            self.db.rollback()
            return False
        finally: SessionLocal.remove()

    def eliminar_usuario_completo(self, id_emp):
        try:
            user = self.db.query(Usuario).filter(Usuario.id_empleado == id_emp).first()
            if user: self.db.delete(user)
            emp = self.db.query(Empleado).filter(Empleado.id_empleado == id_emp).first()
            if emp: self.db.delete(emp)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False
        finally:
            SessionLocal.remove()

    def registrar_personal_completo(self, nombre, apellido, codigo_acceso, password, rol):
        """
        IMPORTANTE: El nombre del tercer parámetro debe ser 'codigo_acceso' 
        para que coincida con la vista.
        """
        try:
            # 1. Crear Empleado
            nuevo_empleado = Empleado(
                nombre=nombre, 
                apellido_pat=apellido
            )
            self.db.add(nuevo_empleado)
            self.db.flush() 

            # 2. Crear Usuario vinculado
            nuevo_usuario = Usuario(
                correo=codigo_acceso,  # Aquí guardamos el HLA01 / HLE02
                contrasena=password, 
                rol=rol, 
                id_empleado=nuevo_empleado.id_empleado
            )
            self.db.add(nuevo_usuario)

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f" Error en DAO: {e}")
            return False
        finally:
            SessionLocal.remove()
    def modificar_usuario(self, id_emp, nombre, apellido, codigo_acceso, password, rol):
        try:
            # 1. Buscar los objetos actuales en la base de datos
            emp = self.db.query(Empleado).filter(Empleado.id_empleado == id_emp).first()
            user = self.db.query(Usuario).filter(Usuario.id_empleado == id_emp).first()
            
            if emp and user:
                # 2. Modificar los valores
                emp.nombre = nombre
                emp.apellido_pat = apellido
                
                user.correo = codigo_acceso
                user.rol = rol
                # Solo cambiamos la contraseña si el usuario escribió algo en el campo
                if password:
                    user.contrasena = password
                
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            print(f"⚠️ Error al modificar: {e}")
            return False
        finally:
            SessionLocal.remove()       
            