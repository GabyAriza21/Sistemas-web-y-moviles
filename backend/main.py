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

class ProductoCrear(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=120, example="Pijama Satín Dos Piezas")
    descripcion: Optional[str] = Field(None, max_length=300, example="Conjunto de short y camisa de satín suave")
    precio: float = Field(..., gt=0, example=65000.0)
    stock: int = Field(..., ge=0, example=15)
    id_categoria: int = Field(..., example=2)
    imagen_url: Optional[str] = Field(None, max_length=300, example="https://via.placeholder.com/300")

class ProductoRespuesta(ProductoCrear):
    id_producto: int

# Datos de respaldo (fallback) por si la BD no responde
catalogo_productos = [
    {
        "id_producto": 1,
        "nombre": "Body Encaje Velvet",
        "descripcion": "Body delicado con copa prehormada y detalles en encaje",
        "precio": 55000.0,
        "stock": 12,
        "id_categoria": 1,
        "imagen_url": "asset/bodys.jpeg"
    },
    {
        "id_producto": 2,
        "nombre": "Cachetero Encaje Soft",
        "descripcion": "Cachetero suave sin costuras visibles de alta comodidad",
        "precio": 22000.0,
        "stock": 25,
        "id_categoria": 1,
        "imagen_url": "asset/cachetero.jpeg" 
    },
    {
        "id_producto": 3,
        "nombre": "Set Ropa Interior Glam",
        "descripcion": "Conjunto de dos piezas en encaje fino ajustable",
        "precio": 48000.0,
        "stock": 10,
        "id_categoria": 1,
        "imagen_url": "asset/set de ropa interior.jpeg"
    },
    {
        "id_producto": 4,
        "nombre": "Top Básico Confort",
        "descripcion": "Top de descanso con soporte ligero en tela transpirable",
        "precio": 32000.0,
        "stock": 18,
        "id_categoria": 1,
        "imagen_url": "asset/top.jpeg"
    },
    {
        "id_producto": 5,
        "nombre": "Pijama Satín Clásica",
        "descripcion": "Conjunto de camisa manga larga y pantalón en satín brillante",
        "precio": 75000.0,
        "stock": 15,
        "id_categoria": 2,
        "imagen_url": "asset/pijama.jpeg"
    },
    {
        "id_producto": 6,
        "nombre": "Pijama Cute Algodón",
        "descripcion": "Pijama de short y blusa fresca en 100% algodón suave",
        "precio": 62000.0,
        "stock": 20,
        "id_categoria": 2,
        "imagen_url": "asset/pijama cute.jpeg"
    },
    {
        "id_producto": 7,
        "nombre": "Pijama Pasión Seda",
        "descripcion": "Conjunto premium de descanso con acabados elegantes en seda",
        "precio": 80000.0,
        "stock": 8,
        "id_categoria": 2,
        "imagen_url": "asset/pijama pasion.jpeg"
    },
    {
        "id_producto": 8,
        "nombre": "Combo Set Descanso",
        "descripcion": "Set completo de 3 piezas: bata ligera, blusa y pantalón",
        "precio": 89000.0,
        "stock": 10,
        "id_categoria": 2,
        "imagen_url": "asset/combo set.jpeg"
    }
]

# Endpoints
@app.get("/")
def inicio():
    return {"estado": "Servidor activo", "mensaje": "API de la tienda funcionando"}

@app.get("/api/categorias")
def listar_categorias():
    return [
        {"id_categoria": 1, "nombre": "Ropa Interior y Bodys"},
        {"id_categoria": 2, "nombre": "Pijamas"}
    ]

# AQUI ESTA EL CAMBIO: Consulta en vivo a Oracle APEX
@app.get("/api/productos", response_model=List[ProductoRespuesta])
async def listar_productos():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            respuesta = await client.get(ORDS_URL)
            print(f"--> Código ORDS: {respuesta.status_code}")
            
            if respuesta.status_code == 200:
                datos = respuesta.json()
                items = datos.get("items", [])
                print(f"--> Cantidad de items traídos de Oracle: {len(items)}")
                
                if items:
                    # Normalizamos todas las llaves a minúsculas (nombre, precio, etc.)
                    productos_normalizados = []
                    for item in items:
                        item_min = {k.lower(): v for k, v in item.items()}
                        productos_normalizados.append(item_min)
                    return productos_normalizados
    except Exception as e:
        print(f"--> Error conectando con ORDS: {e}")
    
    print("--> Usando catálogo de respaldo local")
    return catalogo_productos

@app.post("/api/productos", response_model=ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCrear):
    nuevo_id = len(catalogo_productos) + 1
    nuevo_prod = producto.dict()
    nuevo_prod["id_producto"] = nuevo_id
    catalogo_productos.append(nuevo_prod)
    return nuevo_prod