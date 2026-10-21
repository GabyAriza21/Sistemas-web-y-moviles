PANTYS CA BY CLAUDIA ARIZA - Tienda Web

Sistema web integral de comercio electrónico para catálogo, visualización y gestión de pedidos de prendas de lencería y pijamas,con panel de administración para gestión de inventario e indicadores. Desarrollado como proyecto integrador para la asignatura de Sistemas Web y Móviles.

INTEGRANTES DEL EQUIPO Y ROLES

- Gabriela Astorquiza: Base de Datos y Backend — Oracle Database, ORDS, FastAPI, Python, Uvicorn, Pydantic.
- Elizabeth Mina: Maquetación y Diseño Frontend — HTML5, CSS3, Bootstrap 5, Bootstrap Icons.
- Xiomara Calderon: Lógica Frontend e Integración — JavaScript (ES6+), Fetch API, Manejo del DOM.

ARQUITECTURA Y TECNOLOGIAS

- Base de Datos: Oracle Database alojada en la nube, exponiendo recursos mediante ORDS (Oracle REST Data Services).
- Backend: FastAPI (Python 3.10+) actuando como API REST intermedia para procesamiento de datos, validación con Pydantic, cálculo de métricas y soporte de CORS.
- Frontend: Interfaz responsiva desarrollada con Bootstrap 5, JavaScript dinámico para renderizado de catálogo, gestión de carrito de compras y panel de control (Dashboard).

ESTRUCTURA DE BASE DE DATOS Y DOCUMENTACION 

La base de datos relacional consta de 6 tablas organizadas en scripts SQL dentro de la carpeta database/:
1. 01_tables.sql: Definición de tablas y llaves primarias/foráneas (PK/FK).
2. 02_constraints.sql: Restricciones de integridad, campos no nulos y validaciones.
3. 03_data.sql: Datos semilla iniciales para pruebas del sistema.
4. 04_queries.sql: Consultas consolidadas, joins y reportes.

ENDPOINTS DEL BACKEND 

- Autenticacion: 
POST /api/auth/login: Validación de credenciales y retorno de rol.

- Productos (CRUD):
 GET /api/productos: Obtener catálogo de productos.
  GET /api/productos/{id}: Obtener detalle de un producto.
  POST /api/productos: Crear un nuevo producto.
  PUT /api/productos/{id}: Actualizar un producto existente.
  DELETE /api/productos/{id}: Eliminar un producto.

- Pedidos: 
POST /api/pedidos: Registrar una orden de compra desde el carrito.

- Dashboard / Indicadores:
GET /api/dashboard: Obtener métricas consolidadas (ventas, pedidos, total productos y alertas de stock bajo).

INSTRUCCIONES DE EJECUCION LOCAL
1. Clonar el repositorio 
git clone [https://github.com/GabyAriza21/Sistemas-web-y-moviles.git](https://github.com/GabyAriza21/Sistemas-web-y-moviles.git)
cd Sistemas-web-y-moviles

2. iniciar el backend (FastAPI)
cd backend
pip install -r requirements.txt 
uvicorn main:app --reload --port 8000

3. iniciar el fronted
- Abrir carpeta fronted/
- iniciar archivo index.html (extension live server puerto 5500) o directamente desde el navegador
- control s para guardar

