from datetime import date
from modelos.factura import Factura


class Delivery:

    ESTADOS_VALIDOS = ("pendiente", "en_camino", "entregado", "cancelado")

    def __init__(
        self,
        id: int,
        factura: Factura,
        direccion: str,
        estado: str = "pendiente",
        fecha_entrega: date | None = None,
    ):
        self.id = id
        self.factura = factura
        self.direccion = direccion
        self.estado = estado
        self.fecha_entrega = fecha_entrega


    def marcar_entregado(self) -> None:
        self.estado = "entregado"
        self.fecha_entrega = date.today()

    def esta_pendiente(self) -> bool:
        return self.estado == "pendiente"

    def __repr__(self):
        return f"Delivery(id={self.id}, estado='{self.estado}', direccion='{self.direccion}')"
