from modelos.postre import Postre
from modelos.categoria import Categoria


class PostreServicio:

    def __init__(self, postres: list[Postre], categorias: list[Categoria]):
        self._postres = postres
        self._categorias = categorias
        self._siguiente_id = len(postres) + 1

    def obtener_postres(self) -> list[Postre]:
        return list(self._postres)


    def registrar_postre(
        self,
        categoria_id: int,
        nombre: str,
        precio: float,
        disponible: bool = True,
    ) -> tuple[Postre | None, str | None]:

        if not nombre:
            return None, "El nombre del postre es obligatorio"

        if not Postre.validar_precio(precio):
            return None, "El precio debe ser un número mayor o igual a 0"

        categoria = self._buscar_categoria(categoria_id)
        if categoria is None:
            return None, f"No existe la categoría con id {categoria_id}"

        postre = Postre(
            id=self._siguiente_id,
            categoria=categoria,
            nombre=nombre,
            descripcion="",
            precio=precio,
            disponible=disponible,
        )
        self._postres.append(postre)
        self._siguiente_id += 1
        return postre, None

    def cambiar_disponibilidad(
        self, postre_id: int, disponible: bool
    ) -> tuple[Postre | None, str | None]:
        postre = self._buscar_postre(postre_id)
        if postre is None:
            return None, f"No existe un postre con id {postre_id}"

        postre.cambiar_disponibilidad(disponible)
        return postre, None


    def _buscar_postre(self, postre_id: int) -> Postre | None:
        for p in self._postres:
            if p.id == postre_id:
                return p
        return None

    def _buscar_categoria(self, categoria_id: int) -> Categoria | None:
        for c in self._categorias:
            if c.id == categoria_id:
                return c
        return None
