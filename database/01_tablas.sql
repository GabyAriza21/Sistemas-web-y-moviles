-- Tabla de Roles
CREATE TABLE roles (
    id_rol NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_rol VARCHAR2(50) NOT NULL UNIQUE
);

-- Tabla de Usuarios
CREATE TABLE usuarios (
    id_usuario NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    correo VARCHAR2(100) NOT NULL UNIQUE,
    clave VARCHAR2(255) NOT NULL,
    id_rol NUMBER NOT NULL,
    CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- Tabla de Categorias
CREATE TABLE categorias (
    id_categoria NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_categoria VARCHAR2(50) NOT NULL UNIQUE,
    descripcion VARCHAR2(200)
);

-- Tabla de Productos
CREATE TABLE productos (
    id_producto NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(120) NOT NULL,
    descripcion VARCHAR2(300),
    precio NUMBER(10, 2) NOT NULL CHECK (precio > 0),
    stock NUMBER NOT NULL CHECK (stock >= 0),
    id_categoria NUMBER NOT NULL,
    imagen_url VARCHAR2(300),
    CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

-- Tabla de Pedidos
CREATE TABLE pedidos (
    id_pedido NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario NUMBER NOT NULL,
    fecha_pedido DATE DEFAULT SYSDATE NOT NULL,
    total NUMBER(10, 2) DEFAULT 0 NOT NULL,
    estado VARCHAR2(30) DEFAULT 'Pendiente' NOT NULL,
    CONSTRAINT fk_pedido_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla de Detalles del Pedido
CREATE TABLE detalles_pedido (
    id_detalle NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pedido NUMBER NOT NULL,
    id_producto NUMBER NOT NULL,
    cantidad NUMBER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMBER(10, 2) NOT NULL,
    CONSTRAINT fk_detalle_pedido FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    CONSTRAINT fk_detalle_producto FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

