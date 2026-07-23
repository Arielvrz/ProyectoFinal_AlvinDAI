from datetime import date
from modelos.rol import Rol


class Empleado:

    def __init__(
        self,
        id: int,
        nombre: str,
        apellido: str,
        email: str,
        clave: str,
        telefono: str,
        rol: Rol,
        fecha_contratacion: date | None = None,
    ):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.clave = clave
        self.telefono = telefono
        self.rol = rol
        self.fecha_contratacion = fecha_contratacion or date.today()

    def validar_credenciales(self, clave: str) -> bool:
        return self.clave == clave

    def es_admin(self) -> bool:
        return self.rol.nombre.lower() == "admin"

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __repr__(self):
        return f"Empleado(id={self.id}, nombre='{self.nombre_completo()}', rol='{self.rol.nombre}')"
