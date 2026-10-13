const API_URL = "https://psychic-barnacle-v6r7gqg69pwx2xrp-8000.app.github.dev/api/productos";
let carrito = [];
let todosLosProductos = [];

// 1. Obtener catálogo desde FastAPI
async function cargarCatalogo() {
    try {
        const respuesta = await fetch(API_URL);
        if (!respuesta.ok) throw new Error(`HTTP error! status: ${respuesta.status}`);
        todosLosProductos = await respuesta.json();
        mostrarProductos(todosLosProductos);
    } catch (error) {
        console.error("Error al conectar con la API:", error);
    }
}

// 2. Renderizar tarjetas de productos
function mostrarProductos(productos) {
    const contenedor = document.getElementById("contenedor-productos");
    if (!contenedor) return;
    contenedor.innerHTML = "";

    if (!productos || productos.length === 0) {
        contenedor.innerHTML = `<div class="col-12 text-center text-muted py-5">No hay productos disponibles en esta categoría.</div>`;
        return;
    }

    productos.forEach(prod => {
        const id = prod.id_producto || prod.ID_PRODUCTO;
        const nombre = prod.nombre || prod.NOMBRE || 'Producto';
        const descripcion = prod.descripcion || prod.DESCRIPCION || '';
        const precio = Number(prod.precio || prod.PRECIO || 0);
        const imagen = prod.imagen_url || prod.IMAGEN_URL || 'asset/bodys.jpeg';

        const col = document.createElement("div");
        col.className = "col";
        col.innerHTML = `
            <div class="card h-100 shadow-sm border-0">
                <img src="${imagen}" class="card-img-top" alt="${nombre}" style="height: 250px; object-fit: cover;" onerror="this.src='https://via.placeholder.com/300x200?text=Prenda'">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title fs-6 fw-bold text-dark">${nombre}</h5>
                    <p class="card-text text-muted small flex-grow-1">${descripcion}</p>
                    <p class="fw-bold fs-5 text-primary mb-2">$${precio.toLocaleString('es-CO')}</p>
                    
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Talla:</label>
                        <select class="form-select form-select-sm" id="talla-${id}">
                            <option value="S">S</option>
                            <option value="M" selected>M</option>
                            <option value="L">L</option>
                        </select>
                    </div>

                    <button class="btn btn-dark mt-auto w-100" onclick="agregarAlCarrito('${nombre}', ${precio}, 'talla-${id}')">
                        Agregar al Carrito
                    </button>
                </div>
            </div>
        `;
        contenedor.appendChild(col);
    });
}

// 3. Filtrar por categoría dinámica
function filtrarCategoria(tipo, boton) {
    document.querySelectorAll(".btn-group button").forEach(b => b.classList.remove("active"));
    boton.classList.add("active");

    if (tipo === "todos") {
        mostrarProductos(todosLosProductos);
    } else if (tipo === "ropa-interior") {
        // Filtra por id_categoria 1 o nombre que contenga "Ropa Interior"
        mostrarProductos(todosLosProductos.filter(p => p.id_categoria === 1));
    } else if (tipo === "pijamas") {
        // Filtra por la categoría que no sea 1 (pijamas)
        mostrarProductos(todosLosProductos.filter(p => p.id_categoria !== 1));
    }
}

// 4. Gestión del Carrito
function agregarAlCarrito(nombre, precio, idSelectTalla) {
    const talla = document.getElementById(idSelectTalla).value;
    carrito.push({ nombre, precio, talla });
    actualizarCarrito();
}

function actualizarCarrito() {
    const lista = document.getElementById("lista-carrito");
    const conteo = document.getElementById("conteo-carrito");
    const totalElemento = document.getElementById("total-carrito");

    lista.innerHTML = "";
    let total = 0;

    if (carrito.length === 0) {
        lista.innerHTML = `<li class="list-group-item text-muted text-center" id="carrito-vacio">El carrito está vacío</li>`;
    } else {
        carrito.forEach((item, index) => {
            total += item.precio;
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center py-2";
            li.innerHTML = `
                <div>
                    <strong>${item.nombre}</strong> <span class="badge bg-secondary ms-1">${item.talla}</span><br>
                    <span class="text-success small fw-bold">$${item.precio.toLocaleString('es-CO')}</span>
                </div>
                <button class="btn btn-outline-danger btn-sm py-0 px-2" onclick="eliminarDelCarrito(${index})">&times;</button>
            `;
            lista.appendChild(li);
        });
    }

    conteo.innerText = `${carrito.length} ítems`;
    totalElemento.innerText = `$${total.toLocaleString('es-CO')}`;
}

function eliminarDelCarrito(index) {
    carrito.splice(index, 1);
    actualizarCarrito();
}

function confirmarPedido() {
    if (carrito.length === 0) {
        alert("Tu carrito está vacío. Agrega prendas antes de confirmar.");
        return;
    }
    const total = carrito.reduce((sum, item) => sum + item.precio, 0);
    alert(`¡Pedido recibido con éxito!\nTotal a pagar: $${total.toLocaleString('es-CO')}`);
    carrito = [];
    actualizarCarrito();
}

document.addEventListener("DOMContentLoaded", cargarCatalogo);