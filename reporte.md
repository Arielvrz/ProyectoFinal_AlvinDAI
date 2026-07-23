# Reporte de Negocio: Valor del Backend en Fragola Inv 2.0

Este reporte express describe cómo el diseño técnico del backend y las reglas de negocio implementadas se traducen en valor tangible para la panadería **Fragola** y su cliente final.

---

## 1. Traducción de lo Técnico a Negocio

En el desarrollo de software, cada línea de código debe responder a una necesidad comercial. A continuación se traduce la arquitectura del sistema al impacto operativo diario de la panadería:

| Componente Técnico | ¿Qué hace en el código? | Traducción al Negocio (Valor) |
| :--- | :--- | :--- |
| **Control de Insumos y Stock Mínimo** | Evalúa si la cantidad del insumo está por debajo del límite (`esta_en_alerta()`). | **Prevención de Pérdidas de Venta:** Evita que la panadería se quede sin materia prima crítica (harina, huevos) en mitad de la producción, eliminando el riesgo de decirle a un cliente: *"No podemos hacer su pastel porque no tenemos ingredientes"*. |
| **Gestión de Movimientos** | Registra entradas y salidas con motivos asociados (`es_entrada()`, `es_salida()`). | **Control de Merma y Auditoría:** Permite detectar fugas de materia prima, desperdicios por caducidad o robos hormiga, optimizando los costos de operación. |
| **Disponibilidad de Postres** | Habilita o deshabilita la venta comercial de un producto (`cambiar_disponibilidad()`). | **Sincronización Comercial:** Evita vender productos agotados. Si un postre del catálogo se queda sin existencias o no está listo para la venta, se desactiva al instante, protegiendo la reputación del negocio. |
| **Módulo de Facturación** | Genera facturas, calcula totales y asocia clientes y empleados. | **Agilidad en Caja:** Automatiza el cobro rápido y sin errores matemáticos en el punto de venta, reduciendo las colas de espera. |

---

## 2. El Valor de la Transaccionalidad Segura para el Cliente Final

La **transaccionalidad segura** (reglas estrictas que impiden operaciones inválidas en el código) no es solo un capricho técnico de calidad de código; es la base de la experiencia y lealtad del cliente.

Así es como las validaciones técnicas benefician directamente al cliente de la panadería:

### A. Consistencia y Confianza (Cero Falsas Promesas)
* **La regla técnica:** El sistema bloquea automáticamente la adición de un postre inactivo (`disponible = False`) a una factura.
* **El valor para el cliente:** Elimina la frustración del cliente de ordenar, pagar un postre y que minutos después un empleado le diga: *"Disculpe, nos cobramos esto pero ya no tenemos en vitrina"*. El cliente tiene la certeza de que si el sistema lo factura, el postre está físicamente reservado para él.

### B. Transparencia y Cobro Justo
* **La regla técnica:** El cálculo del subtotal (`cantidad * precio_unitario`) e incremento automático del total de la factura están blindados en el dominio.
* **El valor para el cliente:** El cliente recibe un comprobante exacto y transparente. Se evitan errores humanos del cajero al calcular sumas complejas (especialmente en pedidos grandes), lo que previene cobros excesivos que dañan la confianza o cobros menores que afectan la rentabilidad de la pastelería.

### C. Eficiencia del Servicio y Cero Retrabajo
* **La regla técnica:** No se pueden agregar líneas a una factura que ya ha sido anulada.
* **El valor para el cliente:** Garantiza que los procesos de devolución, cancelación de comandas o reembolsos sean limpios y unidireccionales. El cliente no sufrirá retrasos en caja debido a confusión de tickets o facturas duplicadas en el sistema.

### D. Garantía de Entrega de Pedidos Especiales
* **La regla técnica:** Al realizar un pedido de producción, el consumo de insumos descuenta el inventario y alerta si se cae en stock mínimo.
* **El valor para el cliente:** Si un cliente encarga un pastel de bodas para el sábado, la panadería cuenta con la seguridad de que los ingredientes necesarios ya fueron validados y reservados en el almacén, garantizando la entrega a tiempo de su encargo especial.
