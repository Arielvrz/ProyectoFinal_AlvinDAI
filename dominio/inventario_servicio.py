from modelos.insumo import Insumo
from modelos.empleado import Empleado
from modelos.movimiento import Movimiento


class InventarioServicio:

    def __init__(
        self,
        insumos: list[Insumo],
        empleados: list[Empleado],
        movimientos: list[Movimiento],
    ):
        self._insumos = insumos
        self._empleados = empleados
        self._movimientos = movimientos
        self._siguiente_id = len(movimientos) + 1


    def obtener_inventario(self) -> list[Insumo]:
        return list(self._insumos)

    def obtener_alertas(self) -> list[Insumo]:
        return [i for i in self._insumos if i.esta_en_alerta()]


    def registrar_movimiento(
        self,
        insumo_id: int,
        empleado_id: int,
        tipo: str,
        cantidad: float,
        motivo: str,
    ) -> tuple[dict | None, str | None]:

        empleado = self._buscar_empleado(empleado_id)
        if empleado is None:
            return None, "Empleado no autorizado o inexistente"

        insumo = self._buscar_insumo(insumo_id)
        if insumo is None:
            return None, f"No existe el insumo con id {insumo_id}"

        if tipo not in Movimiento.TIPOS_VALIDOS:
            return None, "El tipo de movimiento debe ser 'entrada' o 'salida'"

        try:
            if tipo == "entrada":
                insumo.aplicar_entrada(cantidad)
            else:
                insumo.aplicar_salida(cantidad)
        except ValueError as e:
            return None, str(e)

        movimiento = Movimiento(
            id=self._siguiente_id,
            insumo=insumo,
            empleado=empleado,
            tipo=tipo,
            cantidad=cantidad,
            motivo=motivo,
        )
        self._movimientos.append(movimiento)
        self._siguiente_id += 1

        resultado = {
            "movimiento": movimiento,
            "insumo_actualizado": insumo,
            "alerta_stock_minimo": insumo.esta_en_alerta(),
        }
        return resultado, None


    def _buscar_insumo(self, insumo_id: int) -> Insumo | None:
        for ins in self._insumos:
            if ins.id == insumo_id:
                return ins
        return None

    def _buscar_empleado(self, empleado_id: int) -> Empleado | None:
        for emp in self._empleados:
            if emp.id == empleado_id:
                return emp
        return None
