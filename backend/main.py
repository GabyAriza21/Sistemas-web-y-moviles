from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Boutique & Calzado",
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

@app.get("/")
def inicio():
    return {"estado": "Servidor activo", "mensaje": "API de la tienda funcionando"}

@app.get("/api/categorias")
def listar_categorias():
    return [
        {"id_categoria": 1, "nombre": "Ropa Interior y Bodys"},
        {"id_categoria": 2, "nombre": "Pijamas"}
    ]
