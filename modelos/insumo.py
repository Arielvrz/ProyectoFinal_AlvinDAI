class Insumo:

    def __init__(
        self,
        id: int,
        nombre: str,
        unidad: str,
        cantidad: float,
        stock_minimo: float,
    ):
        self.id = id
        self.nombre = nombre
        self.unidad = unidad
        self.cantidad = cantidad
        self.stock_minimo = stock_minimo

    def esta_en_alerta(self) -> bool:
        return self.cantidad <= self.stock_minimo

    def tiene_stock_suficiente(self, cantidad: float) -> bool:
        return self.cantidad >= cantidad

    def aplicar_entrada(self, cantidad: float) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad de entrada debe ser mayor a 0")
        self.cantidad += cantidad

    def aplicar_salida(self, cantidad: float) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad de salida debe ser mayor a 0")
        if not self.tiene_stock_suficiente(cantidad):
            raise ValueError(
                f"Stock insuficiente de '{self.nombre}': "
                f"disponible {self.cantidad}, solicitado {cantidad}"
            )
        self.cantidad -= cantidad

    def __repr__(self):
        return f"Insumo(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad} {self.unidad})"
