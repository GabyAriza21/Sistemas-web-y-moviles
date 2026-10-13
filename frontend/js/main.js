const API_URL = "https://psychic-barnacle-v6r7gqg69pwx2xrp-8000.app.github.dev/api/productos";
let carrito = [];
let todosLosProductos = [];

// Cargar catálogo desde FastAPI
async function cargarCatalogo() {
    try {
        const respuesta = await fetch(API_URL);
        todosLosProductos = await respuesta.json();
        mostrarProductos(todosLosProductos);
    } catch (error) {
        console.error("Error al conectar con la API:", error);
    }
}

// Pintar tarjetas dinámicas
function mostrarProductos(productos) {
    const contenedor = document.getElementById("contenedor-productos");
    if (!contenedor) return;
    contenedor.innerHTML = "";

    productos.forEach(prod => {
        const col = document.createElement("div");
        col.className = "col";
        col.innerHTML = `
            <div class="card h-100 shadow-sm card-producto">
                <img src="${prod.imagen_url}" class="card-img-top" alt="${prod.nombre}" style="height: 250px; object-fit: cover;" onerror="this.src='https://via.placeholder.com/300x200?text=Prenda'">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${prod.nombre}</h5>
                    <p class="card-text text-muted mb-1 small flex-grow-1">${prod.descripcion || ''}</p>
                    <p class="fw-bold fs-5 text-primary mb-2">$${prod.precio.toLocaleString('es-CO')}</p>
                    
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Talla:</label>
                        <select class="form-select form-select-sm" id="talla-${prod.id_producto}">
                            <option value="S">S</option>
                            <option value="M" selected>M</option>
                            <option value="L">L</option>
                        </select>
                    </div>

                    <button class="btn btn-success mt-auto w-100" onclick="agregarAlCarrito('${prod.nombre}', ${prod.precio}, 'talla-${prod.id_producto}')">
                        Agregar al Carrito
                    </button>
                </div>
            </div>
        `;
        contenedor.appendChild(col);
    });
}

// Filtrar por categoría
function filtrarCategoria(tipo, boton) {
    document.querySelectorAll(".btn-group button").forEach(b => b.classList.remove("active"));
    boton.classList.add("active");

    if (tipo === "todos") {
        mostrarProductos(todosLosProductos);
    } else if (tipo === "ropa-interior") {
        mostrarProductos(todosLosProductos.filter(p => p.id_categoria === 1));
    } else if (tipo === "pijamas") {
        mostrarProductos(todosLosProductos.filter(p => p.id_categoria === 2));
    }
}

// Lógica del Carrito
function agregarAlCarrito(nombre, precio, idTalla) {
    const talla = document.getElementById(idTalla).value;
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
        lista.innerHTML = `<li class="list-group-item text-muted text-center">El carrito está vacío</li>`;
    } else {
        carrito.forEach((item, index) => {
            total += item.precio;
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center small";
            li.innerHTML = `
                <div>
                    <strong>${item.nombre}</strong> (Talla: ${item.talla})<br>
                    <span class="text-success">$${item.precio.toLocaleString('es-CO')}</span>
                </div>
                <button class="btn btn-outline-danger btn-sm py-0 px-1" onclick="eliminarDelCarrito(${index})">&times;</button>
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
        alert("El carrito está vacío.");
        return;
    }
    alert("¡Pedido realizado con éxito!");
    carrito = [];
    actualizarCarrito();
}

document.addEventListener("DOMContentLoaded", cargarCatalogo);