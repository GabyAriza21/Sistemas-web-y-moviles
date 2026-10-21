from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import httpx

app = FastAPI(
    title="API Boutique & Pijamas",
    description="Servidor backend para el proyecto integrador",
    version="1.0"
)

# Permitir peticiones desde el frontend sin bloqueos CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL generada en Oracle APEX (Módulo tienda / productos)
ORDS_URL = "https://oracleapex.com/ords/wenmoviles912189/tienda/productos"

# --- MODELOS DE DATOS (PRODUCTOS) ---
class ProductoCrear(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=120, example="Pijama Satín Dos Piezas")
    descripcion: Optional[str] = Field(None, max_length=300, example="Conjunto de short y camisa de satín suave")
    precio: float = Field(..., gt=0, example=65000.0)
    stock: int = Field(..., ge=0, example=15)
    id_categoria: int = Field(..., example=2)
    imagen_url: Optional[str] = Field(None, max_length=300, example="asset/pijama.jpeg")

class ProductoRespuesta(ProductoCrear):
    id_producto: int

# --- MODELOS DE DATOS (PEDIDOS) ---
class ItemPedido(BaseModel):
    id_producto: int
    nombre: str
    precio: float = Field(..., gt=0)
    cantidad: int = Field(..., ge=1)
    talla: Optional[str] = "M"

class PedidoCrear(BaseModel):
    nombre_cliente: str = Field(..., min_length=3, example="Cliente Mostrador")
    telefono: Optional[str] = Field(None, example="3001234567")
    items: List[ItemPedido]
    total: float = Field(..., gt=0)

# --- MODELO DE DATOS (LOGIN - RÚBRICA PTO 9) ---
class LoginEntrada(BaseModel):
    correo: str = Field(..., example="admin@pantysca.com")
    clave: str = Field(..., example="admin123")

# Catálogo local de respaldo por si falla la red
catalogo_productos = [
    {"id_producto": 1, "nombre": "Body Encaje Velvet", "descripcion": "Body delicado con copa prehormada y detalles en encaje", "precio": 55000.0, "stock": 12, "id_categoria": 1, "imagen_url": "asset/bodys.jpeg"},
    {"id_producto": 2, "nombre": "Cachetero Encaje Soft", "descripcion": "Cachetero suave sin costuras visibles de alta comodidad", "precio": 22000.0, "stock": 25, "id_categoria": 1, "imagen_url": "asset/cachetero.jpeg"},
    {"id_producto": 3, "nombre": "Set Ropa Interior Glam", "descripcion": "Conjunto de dos piezas en encaje fino ajustable", "precio": 48000.0, "stock": 10, "id_categoria": 1, "imagen_url": "asset/set de ropa interior.jpeg"},
    {"id_producto": 4, "nombre": "Top Básico Confort", "descripcion": "Top de descanso con soporte ligero en tela transpirable", "precio": 32000.0, "stock": 18, "id_categoria": 1, "imagen_url": "asset/top.jpeg"},
    {"id_producto": 5, "nombre": "Pijama Satín Clásica", "descripcion": "Conjunto de camisa manga larga y pantalón en satín brillante", "precio": 75000.0, "stock": 15, "id_categoria": 2, "imagen_url": "asset/pijama.jpeg"},
    {"id_producto": 6, "nombre": "Pijama Cute Algodón", "descripcion": "Pijama de short y blusa fresca en 100% algodón suave", "precio": 62000.0, "stock": 20, "id_categoria": 2, "imagen_url": "asset/pijama cute.jpeg"},
    {"id_producto": 7, "nombre": "Pijama Pasión Seda", "descripcion": "Conjunto premium de descanso con acabados elegantes en seda", "precio": 80000.0, "stock": 8, "id_categoria": 2, "imagen_url": "asset/pijama pasion.jpeg"},
    {"id_producto": 8, "nombre": "Combo Set Descanso", "descripcion": "Set completo de 3 piezas: bata ligera, blusa y pantalón", "precio": 89000.0, "stock": 10, "id_categoria": 2, "imagen_url": "asset/combo set.jpeg"}
]

# Usuarios registrados alineados con la BD (Pto 9: Dos roles)
usuarios_sistema = [
    {"id_usuario": 1, "nombre": "Admin Pantys", "correo": "admin@pantysca.com", "clave": "admin123", "rol": "Administrador"},
    {"id_usuario": 2, "nombre": "Cliente Demo", "correo": "cliente@ejemplo.com", "clave": "cliente123", "rol": "Cliente"}
]

# Registro acumulado de pedidos
pedidos_guardados = []

# --- ENDPOINTS EXISTENTES ---

@app.get("/")
def inicio():
    return {"estado": "Servidor activo", "mensaje": "API de Boutique & Pijamas funcionando"}

@app.get("/api/categorias")
def listar_categorias():
    return [
        {"id_categoria": 1, "nombre": "Ropa Interior y Bodys"},
        {"id_categoria": 2, "nombre": "Pijamas"}
    ]

@app.get("/api/productos")
async def listar_productos():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            respuesta = await client.get(ORDS_URL)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                items = datos.get("items", [])
                if items:
                    # Normaliza las claves de ORDS a minúsculas
                    return [{k.lower(): v for k, v in item.items()} for item in items]
    except Exception as e:
        print(f"Aviso ORDS: {e}. Usando catálogo local.")
    return catalogo_productos

@app.post("/api/pedidos", status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: PedidoCrear):
    id_pedido_generado = len(pedidos_guardados) + 101
    nuevo_pedido = {
        "id_pedido": id_pedido_generado,
        "cliente": pedido.nombre_cliente,
        "telefono": pedido.telefono,
        "total": pedido.total,
        "cantidad_articulos": len(pedido.items),
        "items": [item.dict() for item in pedido.items]
    }
    pedidos_guardados.append(nuevo_pedido)
    return {
        "mensaje": "Pedido registrado exitosamente",
        "id_pedido": id_pedido_generado,
        "cliente": pedido.nombre_cliente,
        "total": pedido.total,
        "cantidad_articulos": len(pedido.items)
    }

# --- ENDPOINTS NUEVOS PARA CUMPLIR LA RÚBRICA ---

# 1. Autenticación con 2 roles (Punto 9 de la rúbrica)
@app.post("/api/auth/login")
def login(credenciales: LoginEntrada):
    for u in usuarios_sistema:
        if u["correo"].strip().lower() == credenciales.correo.strip().lower() and u["clave"] == credenciales.clave:
            return {
                "id_usuario": u["id_usuario"],
                "nombre": u["nombre"],
                "correo": u["correo"],
                "rol": u["rol"],
                "mensaje": "Autenticación satisfactoria"
            }
    raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

# 2. Consultar un producto por ID (Read específico - Punto 8)
@app.get("/api/productos/{id_producto}")
def obtener_producto(id_producto: int):
    for p in catalogo_productos:
        if p["id_producto"] == id_producto:
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# 3. Actualizar producto (Update - Puntos 4 y 8)
@app.put("/api/productos/{id_producto}")
def actualizar_producto(id_producto: int, producto_actualizado: ProductoCrear):
    for i, p in enumerate(catalogo_productos):
        if p["id_producto"] == id_producto:
            catalogo_productos[i] = {"id_producto": id_producto, **producto_actualizado.dict()}
            return {"mensaje": "Producto modificado con éxito", "producto": catalogo_productos[i]}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# 4. Eliminar producto (Delete - Puntos 4 y 8)
@app.delete("/api/productos/{id_producto}")
def eliminar_producto(id_producto: int):
    for i, p in enumerate(catalogo_productos):
        if p["id_producto"] == id_producto:
            eliminado = catalogo_productos.pop(i)
            return {"mensaje": f"Producto '{eliminado['nombre']}' eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# 5. Dashboard con indicadores calculados (Punto 4 de la rúbrica)
@app.get("/api/dashboard")
def dashboard_indicadores():
    total_ventas = sum(p["total"] for p in pedidos_guardados)
    return {
        "total_productos": len(catalogo_productos),
        "total_pedidos": len(pedidos_guardados),
        "total_ventas": total_ventas,
        "productos_stock_bajo": len([p for p in catalogo_productos if p["stock"] <= 10])
    }