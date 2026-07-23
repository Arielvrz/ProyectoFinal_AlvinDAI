class Categoria:

    def __init__(self, id: int, nombre: str, descripcion: str = ""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre='{self.nombre}')"
