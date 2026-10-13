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

# --- ENDPOINTS ---

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
    # Genera un ID simulado para confirmar la orden recibida
    id_pedido_generado = 101
    return {
        "mensaje": "Pedido registrado exitosamente",
        "id_pedido": id_pedido_generado,
        "cliente": pedido.nombre_cliente,
        "total": pedido.total,
        "cantidad_articulos": len(pedido.items)
    }