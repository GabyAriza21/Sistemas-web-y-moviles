// URL de tu Backend en FastAPI
const API_URL = "https://psychic-barnacle-v6r7gqg69pwx2xrp-8000.app.github.dev/api";

let todosLosProductos = [];
let carrito = [];

// 1. Cargar productos desde el backend
async function cargarCatalogo() {
    try {
        const respuesta = await fetch(`${API_URL}/productos`);
        todosLosProductos = await respuesta.json();
        mostrarProductos(todosLosProductos);
    } catch (error) {
        console.error("Error al cargar el catálogo:", error);
        const contenedor = document.getElementById("contenedor-productos");
        if (contenedor) {
            contenedor.innerHTML = `<div class="col-12 text-center text-danger"><p>No se pudo conectar con el servidor.</p></div>`;
        }
    }
}

// 2. Renderizar los productos en las tarjetas de Bootstrap
function mostrarProductos(productos) {
    const contenedor = document.getElementById("contenedor-productos");
    if (!contenedor) return;

    contenedor.innerHTML = "";

    if (productos.length === 0) {
        contenedor.innerHTML = `<div class="col-12 text-center text-muted"><p>No hay productos en esta categoría.</p></div>`;
        return;
    }

    productos.forEach(producto => {
        let rutaImg = producto.imagen_url || "";
        const precioFormateado = Number(producto.precio).toLocaleString("es-CO");

        contenedor.innerHTML += `
            <div class="col">
                <div class="card h-100 shadow-sm border-0">
                    <img src="${rutaImg}" 
                         class="card-img-top" 
                         alt="${producto.nombre}" 
                         style="height: 220px; object-fit: cover; cursor: zoom-in;" 
                         onclick="ampliarImagen('${rutaImg}', '${producto.nombre}')" 
                         onerror="this.onerror=null; this.src='https://placehold.co/300x220?text=Foto+Producto';">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title fw-bold fs-6">${producto.nombre}</h5>
                        <p class="card-text text-muted small flex-grow-1">${producto.descripcion || ''}</p>
                        <div class="d-flex justify-content-between align-items-center mt-3">
                            <span class="fs-5 fw-bold text-success">$${precioFormateado}</span>
                            <button class="btn btn-outline-primary btn-sm" onclick='agregarAlCarrito(${JSON.stringify(producto)})'>
                                <i class="bi bi-cart-plus"></i> Agregar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}

// 3. Filtros de Categorías
function filtrarCategoria(categoria, boton) {
    if (boton) {
        document.querySelectorAll(".btn-group button").forEach(b => b.classList.remove("active"));
        boton.classList.add("active");
    }

    if (categoria === 'todos') {
        mostrarProductos(todosLosProductos);
    } else if (categoria === 'ropa-interior') {
        mostrarProductos(todosLosProductos.filter(p => p.id_categoria === 1));
    } else if (categoria === 'pijamas') {
        mostrarProductos(todosLosProductos.filter(p => p.id_categoria === 2));
    }
}

// 4. Lógica del Carrito
function agregarAlCarrito(producto) {
    carrito.push(producto);
    actualizarCarritoUI();
}

function actualizarCarritoUI() {
    const conteo = document.getElementById("conteo-carrito");
    const lista = document.getElementById("lista-carrito");
    const totalEl = document.getElementById("total-carrito");

    if (conteo) conteo.innerText = `${carrito.length} ítems`;

    if (!lista || !totalEl) return;

    if (carrito.length === 0) {
        lista.innerHTML = `<li class="list-group-item text-muted text-center" id="carrito-vacio">El carrito está vacío</li>`;
        totalEl.innerText = "\$0";
        return;
    }

    lista.innerHTML = "";
    let total = 0;

    carrito.forEach((item) => {
        total += item.precio;
        lista.innerHTML += `
            <li class="list-group-item d-flex justify-content-between align-items-center px-2 py-1">
                <span class="small text-truncate" style="max-width: 140px;">${item.nombre}</span>
                <span class="badge bg-secondary rounded-pill">$${Number(item.precio).toLocaleString('es-CO')}</span>
            </li>
        `;
    });

    totalEl.innerText = `$${total.toLocaleString('es-CO')}`;
}

// 5. Enviar Pedido al Backend (POST /api/pedidos)
async function confirmarPedido() {
    if (carrito.length === 0) {
        alert("El carrito está vacío. Agrega algún producto primero.");
        return;
    }

    const totalCalculado = carrito.reduce((acc, item) => acc + item.precio, 0);

    const pedido = {
        nombre_cliente: "Cliente Web",
        telefono: "3000000000",
        items: carrito.map(item => ({
            id_producto: item.id_producto,
            nombre: item.nombre,
            precio: item.precio,
            cantidad: 1,
            talla: "M"
        })),
        total: totalCalculado
    };

    try {
        const res = await fetch(`${API_URL}/pedidos`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(pedido)
        });

        if (res.ok) {
            alert("¡Pedido realizado con éxito!");
            carrito = [];
            actualizarCarritoUI();
        } else {
            alert("Hubo un error al procesar el pedido.");
        }
    } catch (error) {
        console.error("Error al registrar pedido:", error);
        alert("No se pudo conectar con el servidor para registrar el pedido.");
    }
}

// 6. Ampliar imagen al hacer clic
function ampliarImagen(ruta, nombre) {
    const imagenPreview = document.getElementById("imagenGrandePreview");
    const tituloPreview = document.getElementById("tituloImagenGrande");
    
    if (imagenPreview) {
        imagenPreview.src = ruta;
    }
    if (tituloPreview) {
        tituloPreview.innerText = nombre;
    }
    
    const modalElement = document.getElementById('modalImagenGrande');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

// Iniciar al cargar el documento
document.addEventListener("DOMContentLoaded", cargarCatalogo);