# PANTYS CA BY CLAUDIA ARIZA - Tienda Web

Sistema web integral de comercio electrónico para catálogo, visualización y gestión de pedidos de prendas de lencería y pijamas. Desarrollado como proyecto integrador para la asignatura de Sistemas Web y Móviles.

## Integrantes del Equipo y Roles

Gabriela Astorquiza: Base de Datos y Backend, Oracle APEX, ORDS, FastAPI, PythonUvicorn Pydantic 
Elizabeth: Maquetación y Diseño Frontend HTML5, CSS3, Bootstrap 5, Bootstrap Icons 
Xiomara: Lógica Frontend y Integración JavaScript (ES6+), Fetch API, DOM Manipulation 

## Arquitectura y Tecnologías

- Base de Datos: Oracle APEX alojado en la nube, exponiendo recursos mediante ORDS (Oracle REST Data Services).
- Backend:FastAPI(Python 3.10+) actuando como API intermedia para consumo seguro de datos, validación con esquemas Pydantic y soporte de CORS.
- Frontend: Interfaz responsiva desarrollada con Bootstrap 5, JavaScript modular para renderizado dinámico del catálogo, cálculo en tiempo real del carrito y modales interactivos para visualización detallada de prendas.

## Endpoints del Backend

`GET` `/`: Comprobación de estado del servicio
`GET` `/api/productos`: Obtiene el listado completo de productos desde oracle 
`POST` `/api/pedidos`: Registra una orden de compra con los ítems dell carrito

## Instrucciones de Ejecución Local
## 1. Clonar el repositorio 
```bash
git clone [https://github.com/GabyAriza21/Sistemas-web-y-moviles.git](https://github.com/GabyAriza21/Sistemas-web-y-moviles.git)
cd Sistemas-web-y-moviles