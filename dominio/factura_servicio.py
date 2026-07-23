from modelos.factura import Factura
from modelos.detalle_factura import DetalleFactura
from modelos.cliente import Cliente
from modelos.empleado import Empleado
from modelos.postre import Postre


class FacturaServicio:

    def __init__(
        self,
        facturas: list[Factura],
        clientes: list[Cliente],
        empleados: list[Empleado],
        postres: list[Postre],
    ):
        self._facturas = facturas
        self._clientes = clientes
        self._empleados = empleados
        self._postres = postres
        self._siguiente_id_factura = len(facturas) + 1
        self._siguiente_id_detalle = 1


    def crear_factura(
        self, cliente_id: int, empleado_id: int
    ) -> tuple[Factura | None, str | None]:

        cliente = self._buscar_cliente(cliente_id)
        if cliente is None:
            return None, f"No existe el cliente con id {cliente_id}"

        empleado = self._buscar_empleado(empleado_id)
        if empleado is None:
            return None, f"No existe el empleado con id {empleado_id}"

        factura = Factura(
            id=self._siguiente_id_factura,
            cliente=cliente,
            empleado=empleado,
        )
        self._facturas.append(factura)
        self._siguiente_id_factura += 1
        return factura, None

    def agregar_linea(
        self, factura_id: int, postre_id: int, cantidad: int
    ) -> tuple[DetalleFactura | None, str | None]:

        factura = self._buscar_factura(factura_id)
        if factura is None:
            return None, f"No existe la factura con id {factura_id}"

        if factura.estado == "anulada":
            return None, "No se pueden agregar líneas a una factura anulada"

        postre = self._buscar_postre(postre_id)
        if postre is None:
            return None, f"No existe el postre con id {postre_id}"

        if not postre.disponible:
            return None, f"El postre '{postre.nombre}' no está disponible"

        if cantidad <= 0:
            return None, "La cantidad debe ser mayor a 0"

        detalle = DetalleFactura(
            id=self._siguiente_id_detalle,
            postre=postre,
            cantidad=cantidad,
            precio_unitario=postre.precio,
        )
        factura.agregar_detalle(detalle)
        self._siguiente_id_detalle += 1
        return detalle, None

    def anular_factura(self, factura_id: int) -> tuple[Factura | None, str | None]:
        factura = self._buscar_factura(factura_id)
        if factura is None:
            return None, f"No existe la factura con id {factura_id}"

        try:
            factura.anular()
        except ValueError as e:
            return None, str(e)

        return factura, None


    def _buscar_factura(self, factura_id: int) -> Factura | None:
        for f in self._facturas:
            if f.id == factura_id:
                return f
        return None

    def _buscar_cliente(self, cliente_id: int) -> Cliente | None:
        for c in self._clientes:
            if c.id == cliente_id:
                return c
        return None

    def _buscar_empleado(self, empleado_id: int) -> Empleado | None:
        for e in self._empleados:
            if e.id == empleado_id:
                return e
        return None

    def _buscar_postre(self, postre_id: int) -> Postre | None:
        for p in self._postres:
            if p.id == postre_id:
                return p
        return None
