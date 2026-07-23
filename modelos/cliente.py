class Cliente:

    def __init__(
        self,
        id: int,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        direccion: str,
    ):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.direccion = direccion


    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre_completo()}')"
