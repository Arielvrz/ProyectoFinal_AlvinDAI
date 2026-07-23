from modelos.empleado import Empleado


class AutenticacionServicio:

    def __init__(self, empleados: list[Empleado]):
        self._empleados = empleados

    def iniciar_sesion(self, email: str, clave: str) -> tuple[Empleado | None, str | None]:
        empleado = self._buscar_por_email(email)

        if empleado is None:
            return None, "No existe un empleado con ese correo"

        if not empleado.validar_credenciales(clave):
            return None, "Contraseña incorrecta"

        return empleado, None

    def es_empleado_valido(self, empleado_id: int) -> bool:
        return self._buscar_por_id(empleado_id) is not None

    def _buscar_por_email(self, email: str) -> Empleado | None:
        for emp in self._empleados:
            if emp.email == email:
                return emp
        return None

    def _buscar_por_id(self, empleado_id: int) -> Empleado | None:
        for emp in self._empleados:
            if emp.id == empleado_id:
                return emp
        return None
