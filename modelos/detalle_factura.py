from modelos.postre import Postre


class DetalleFactura:

    def __init__(
        self,
        id: int,
        postre: Postre,
        cantidad: int,
        precio_unitario: float,
    ):
        self.id = id
        self.postre = postre
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.factura = None


    def calcular_subtotal(self) -> float:
        return self.cantidad * self.precio_unitario

    def __repr__(self):
        return (
            f"DetalleFactura(id={self.id}, postre='{self.postre.nombre}', "
            f"cantidad={self.cantidad}, subtotal={self.calcular_subtotal():.2f})"
        )
