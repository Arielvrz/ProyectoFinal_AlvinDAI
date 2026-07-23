class Rol:

    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    def __repr__(self):
        return f"Rol(id={self.id}, nombre='{self.nombre}')"
