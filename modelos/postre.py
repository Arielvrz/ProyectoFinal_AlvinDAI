from modelos.categoria import Categoria

class Postre:

    def __init__(
        self,
        id: int,
        categoria: Categoria,
        nombre: str,
        descripcion: str,
        precio: float,
        disponible: bool = True,
    ):
        self.id = id
        self.categoria = categoria
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.disponible = disponible

    def cambiar_disponibilidad(self, estado: bool) -> None:
        self.disponible = estado

    @staticmethod
    def validar_precio(precio: float) -> bool:
        return precio is not None and precio >= 0

    def __repr__(self):
        estado = "disponible" if self.disponible else "no disponible"
        return f"Postre(id={self.id}, nombre='{self.nombre}', precio={self.precio}, {estado})"
