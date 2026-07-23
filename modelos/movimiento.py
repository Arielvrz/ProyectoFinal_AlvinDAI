from datetime import datetime
from modelos.insumo import Insumo
from modelos.empleado import Empleado


class Movimiento:

    TIPOS_VALIDOS = ("entrada", "salida")

    def __init__(
        self,
        id: int,
        insumo: Insumo,
        empleado: Empleado,
        tipo: str,
        cantidad: float,
        motivo: str,
        fecha: datetime | None = None,
    ):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de movimiento debe ser 'entrada' o 'salida', se recibió '{tipo}'")

        self.id = id
        self.insumo = insumo
        self.empleado = empleado
        self.tipo = tipo
        self.cantidad = cantidad
        self.motivo = motivo
        self.fecha = fecha or datetime.now()


    def es_entrada(self) -> bool:
        return self.tipo == "entrada"

    def es_salida(self) -> bool:
        return self.tipo == "salida"

    def __repr__(self):
        return (
            f"Movimiento(id={self.id}, tipo='{self.tipo}', "
            f"insumo='{self.insumo.nombre}', cantidad={self.cantidad})"
        )
