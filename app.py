import os
from datetime import date, datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Importar modelos del proyecto
from modelos.rol import Rol
from modelos.empleado import Empleado
from modelos.insumo import Insumo
from modelos.movimiento import Movimiento
from modelos.cliente import Cliente
from modelos.categoria import Categoria
from modelos.postre import Postre
from modelos.detalle_factura import DetalleFactura
from modelos.factura import Factura
from modelos.delivery import Delivery

# Importar servicios del proyecto
from dominio.autenticacion_servicio import AutenticacionServicio
from dominio.inventario_servicio import InventarioServicio
from dominio.postre_servicio import PostreServicio
from dominio.factura_servicio import FacturaServicio

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. DATOS SEMILLA (SEED DATA) EN MEMORIA
# ==========================================
roles = [
    Rol(id=1, nombre="Admin"),
    Rol(id=2, nombre="Empleado")
]

empleados = [
    Empleado(
        id=1,
        nombre="Ariel",
        apellido="Alfaro",
        email="ariel@fragola.com",
        clave="123456",
        telefono="77777777",
        rol=roles[0]  # Admin
    ),
    Empleado(
        id=2,
        nombre="Carlos",
        apellido="Lopez",
        email="carlos@fragola.com",
        clave="password",
        telefono="88888888",
        rol=roles[1]  # Empleado
    )
]

clientes = [
    Cliente(
        id=1,
        nombre="Juan",
        apellido="Perez",
        email="juan@gmail.com",
        telefono="77778888",
        direccion="San Salvador"
    ),
    Cliente(
        id=2,
        nombre="Maria",
        apellido="Gomez",
        email="maria@gmail.com",
        telefono="77779999",
        direccion="La Libertad"
    )
]

categorias = [
    Categoria(id=1, nombre="Pasteles", descripcion="Pasteles enteros para celebraciones"),
    Categoria(id=2, nombre="Repostería", descripcion="Pan dulce, croissants y porciones individuales"),
    Categoria(id=3, nombre="Bebidas", descripcion="Café, infusiones y bebidas frías")
]

postres = [
    Postre(id=1, categoria=categorias[0], nombre="Tres Leches", descripcion="Pastel clásico húmedo de tres leches", precio=25.0, disponible=True),
    Postre(id=2, categoria=categorias[1], nombre="Croissant de Almendras", descripcion="Croissant relleno de crema de almendras", precio=3.5, disponible=True),
    Postre(id=3, categoria=categorias[0], nombre="Cheesecake de Fresa", descripcion="Tarta de queso crema con topping de fresa", precio=22.0, disponible=False)
]

insumos = [
    Insumo(id=1, nombre="Harina de Trigo", unidad="kg", cantidad=50.0, stock_minimo=10.0),
    Insumo(id=2, nombre="Azúcar Refinada", unidad="kg", cantidad=20.0, stock_minimo=5.0),
    Insumo(id=3, nombre="Huevos", unidad="unidades", cantidad=12.0, stock_minimo=24.0),  # Alerta inicial
    Insumo(id=4, nombre="Mantequilla", unidad="kg", cantidad=8.0, stock_minimo=10.0)      # Alerta inicial
]

movimientos = []
facturas = []
deliveries = []

# ==========================================
# 2. INICIALIZACIÓN DE SERVICIOS
# ==========================================
auth_servicio = AutenticacionServicio(empleados)
inventario_servicio = InventarioServicio(insumos, empleados, movimientos)
postre_servicio = PostreServicio(postres, categorias)
factura_servicio = FacturaServicio(facturas, clientes, empleados, postres)

# ==========================================
# 3. FUNCIONES DE SERIALIZACIÓN
# ==========================================
def serialize_rol(r):
    if not r: return None
    return {"id": r.id, "nombre": r.nombre}

def serialize_empleado(e):
    if not e: return None
    return {
        "id": e.id,
        "nombre": e.nombre,
        "apellido": e.apellido,
        "email": e.email,
        "telefono": e.telefono,
        "rol": serialize_rol(e.rol),
        "fecha_contratacion": e.fecha_contratacion.isoformat() if e.fecha_contratacion else None
    }

def serialize_insumo(i):
    if not i: return None
    return {
        "id": i.id,
        "nombre": i.nombre,
        "unidad": i.unidad,
        "cantidad": i.cantidad,
        "stock_minimo": i.stock_minimo,
        "esta_en_alerta": i.esta_en_alerta()
    }

def serialize_movimiento(m):
    if not m: return None
    return {
        "id": m.id,
        "insumo": {"id": m.insumo.id, "nombre": m.insumo.nombre},
        "empleado": {"id": m.empleado.id, "nombre": m.empleado.nombre_completo()},
        "tipo": m.tipo,
        "cantidad": m.cantidad,
        "motivo": m.motivo,
        "fecha": m.fecha.isoformat() if m.fecha else None
    }

def serialize_cliente(c):
    if not c: return None
    return {
        "id": c.id,
        "nombre": c.nombre,
        "apellido": c.apellido,
        "email": c.email,
        "telefono": c.telefono,
        "direccion": c.direccion
    }

def serialize_categoria(cat):
    if not cat: return None
    return {"id": cat.id, "nombre": cat.nombre, "descripcion": cat.descripcion}

def serialize_postre(p):
    if not p: return None
    return {
        "id": p.id,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "precio": p.precio,
        "disponible": p.disponible,
        "categoria": serialize_categoria(p.categoria)
    }

def serialize_detalle_factura(df):
    if not df: return None
    return {
        "id": df.id,
        "postre": {"id": df.postre.id, "nombre": df.postre.nombre},
        "cantidad": df.cantidad,
        "precio_unitario": df.precio_unitario,
        "subtotal": df.calcular_subtotal()
    }

def serialize_factura(f):
    if not f: return None
    return {
        "id": f.id,
        "cliente": serialize_cliente(f.cliente),
        "empleado": {"id": f.empleado.id, "nombre": f.empleado.nombre_completo()},
        "fecha": f.fecha.isoformat() if f.fecha else None,
        "estado": f.estado,
        "detalles": [serialize_detalle_factura(d) for d in f.detalles],
        "total": f.calcular_total()
    }

# ==========================================
# 4. ENDPOINTS DE LA API
# ==========================================

@app.route('/')
def index():
    return jsonify({
        "app": "Fragola Inv API Backend",
        "version": "2.0",
        "endpoints": [
            "POST /api/auth/login",
            "GET /api/inventario",
            "GET /api/inventario/alertas",
            "POST /api/inventario/movimiento",
            "GET /api/postres",
            "POST /api/postres",
            "PATCH /api/postres/<int:postre_id>/disponibilidad",
            "POST /api/facturas",
            "POST /api/facturas/<int:factura_id>/detalles",
            "POST /api/facturas/<int:factura_id>/anular"
        ]
    }), 200

# ----- Autenticación -----
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    clave = data.get('clave')
    
    if not email or not clave:
        return jsonify({"error": "Email y clave son obligatorios"}), 400
        
    empleado, error = auth_servicio.iniciar_sesion(email, clave)
    if error:
        return jsonify({"error": error}), 401
        
    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "empleado": serialize_empleado(empleado)
    }), 200

# ----- Inventario -----
@app.route('/api/inventario', methods=['GET'])
def get_inventario():
    lista = inventario_servicio.obtener_inventario()
    return jsonify([serialize_insumo(i) for i in lista]), 200

@app.route('/api/inventario/alertas', methods=['GET'])
def get_alertas():
    lista = inventario_servicio.obtener_alertas()
    return jsonify([serialize_insumo(i) for i in lista]), 200

@app.route('/api/inventario/movimiento', methods=['POST'])
def post_movimiento():
    data = request.json or {}
    insumo_id = data.get('insumo_id')
    empleado_id = data.get('empleado_id')
    tipo = data.get('tipo')
    cantidad = data.get('cantidad')
    motivo = data.get('motivo', '')
    
    if insumo_id is None or empleado_id is None or not tipo or cantidad is None:
        return jsonify({"error": "insumo_id, empleado_id, tipo y cantidad son obligatorios"}), 400
        
    try:
        cantidad = float(cantidad)
    except ValueError:
        return jsonify({"error": "La cantidad debe ser un número válido"}), 400
        
    res, error = inventario_servicio.registrar_movimiento(
        insumo_id=int(insumo_id),
        empleado_id=int(empleado_id),
        tipo=tipo,
        cantidad=cantidad,
        motivo=motivo
    )
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "mensaje": "Movimiento de inventario registrado con éxito",
        "movimiento": serialize_movimiento(res["movimiento"]),
        "insumo_actualizado": serialize_insumo(res["insumo_actualizado"]),
        "alerta_stock_minimo": res["alerta_stock_minimo"]
    }), 201

# ----- Postres -----
@app.route('/api/postres', methods=['GET'])
def get_postres():
    lista = postre_servicio.obtener_postres()
    return jsonify([serialize_postre(p) for p in lista]), 200

@app.route('/api/postres', methods=['POST'])
def post_postre():
    data = request.json or {}
    categoria_id = data.get('categoria_id')
    nombre = data.get('nombre')
    precio = data.get('precio')
    disponible = data.get('disponible', True)
    
    if categoria_id is None or not nombre or precio is None:
        return jsonify({"error": "categoria_id, nombre y precio son obligatorios"}), 400
        
    try:
        precio = float(precio)
    except ValueError:
        return jsonify({"error": "El precio debe ser un número válido"}), 400
        
    postre, error = postre_servicio.registrar_postre(
        categoria_id=int(categoria_id),
        nombre=nombre,
        precio=precio,
        disponible=bool(disponible)
    )
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "mensaje": "Postre registrado con éxito",
        "postre": serialize_postre(postre)
    }), 201

@app.route('/api/postres/<int:postre_id>/disponibilidad', methods=['PATCH'])
def patch_disponibilidad(postre_id):
    data = request.json or {}
    disponible = data.get('disponible')
    
    if disponible is None:
        return jsonify({"error": "El campo 'disponible' es obligatorio"}), 400
        
    postre, error = postre_servicio.cambiar_disponibilidad(postre_id, bool(disponible))
    if error:
        return jsonify({"error": error}), 404
        
    return jsonify({
        "mensaje": "Disponibilidad del postre actualizada con éxito",
        "postre": serialize_postre(postre)
    }), 200

# ----- Facturación -----
@app.route('/api/facturas', methods=['POST'])
def post_factura():
    data = request.json or {}
    cliente_id = data.get('cliente_id')
    empleado_id = data.get('empleado_id')
    
    if cliente_id is None or empleado_id is None:
        return jsonify({"error": "cliente_id y empleado_id son obligatorios"}), 400
        
    factura, error = factura_servicio.crear_factura(int(cliente_id), int(empleado_id))
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "mensaje": "Factura creada con éxito",
        "factura": serialize_factura(factura)
    }), 201

@app.route('/api/facturas/<int:factura_id>/detalles', methods=['POST'])
def post_detalle(factura_id):
    data = request.json or {}
    postre_id = data.get('postre_id')
    cantidad = data.get('cantidad')
    
    if postre_id is None or cantidad is None:
        return jsonify({"error": "postre_id y cantidad son obligatorios"}), 400
        
    try:
        cantidad = int(cantidad)
    except ValueError:
        return jsonify({"error": "La cantidad debe ser un entero válido"}), 400
        
    detalle, error = factura_servicio.agregar_linea(factura_id, int(postre_id), cantidad)
    if error:
        return jsonify({"error": error}), 400
        
    factura = factura_servicio._buscar_factura(factura_id)
    return jsonify({
        "mensaje": "Línea agregada a la factura con éxito",
        "detalle": serialize_detalle_factura(detalle),
        "factura_actualizada": serialize_factura(factura)
    }), 201

@app.route('/api/facturas/<int:factura_id>/anular', methods=['POST'])
def post_anular(factura_id):
    factura, error = factura_servicio.anular_factura(factura_id)
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "mensaje": "Factura anulada con éxito",
        "factura": serialize_factura(factura)
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Levantamos en todas las interfaces para permitir pruebas locales
    app.run(host='0.0.0.0', port=port, debug=True)
