from datetime import datetime
from modelos.cliente import Cliente
from modelos.empleado import Empleado
from modelos.detalle_factura import DetalleFactura


class Factura:

    ESTADOS_VALIDOS = ("pendiente", "pagada", "anulada")

    def __init__(
        self,
        id: int,
        cliente: Cliente,
        empleado: Empleado,
        fecha: datetime | None = None,
        estado: str = "pendiente",
    ):
        self.id = id
        self.cliente = cliente
        self.empleado = empleado
        self.fecha = fecha or datetime.now()
        self.estado = estado
        self.detalles: list[DetalleFactura] = []


    def calcular_total(self) -> float:
        return sum(d.calcular_subtotal() for d in self.detalles)

    def agregar_detalle(self, detalle: DetalleFactura) -> None:
        detalle.factura = self
        self.detalles.append(detalle)

    def anular(self) -> None:
        if self.estado == "anulada":
            raise ValueError("La factura ya está anulada")
        self.estado = "anulada"

    def __repr__(self):
        return (
            f"Factura(id={self.id}, cliente='{self.cliente.nombre_completo()}', "
            f"total={self.calcular_total():.2f}, estado='{self.estado}')"
        )
