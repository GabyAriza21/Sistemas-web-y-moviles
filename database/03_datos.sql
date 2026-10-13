-- Insercion de roles y categorias de pijamas y bodys
INSERT INTO roles (nombre_rol) VALUES ('Administrador');
INSERT INTO roles (nombre_rol) VALUES ('Cliente');

INSERT INTO categorias (nombre_categoria, descripcion) VALUES ('Ropa Interior y Bodys', 'Prendas intimas y bodys para mujer');

COMMIT; 

-- Inserción de Categorías
INSERT INTO categorias (nombre_categoria, descripcion)
VALUES ('Ropa Interior y Bodys', 'Prendas intimas, bodys y conjuntos comodos');

INSERT INTO categorias (nombre_categoria, descripcion)
VALUES ('Pijamas', 'Pijamas de descanso en seda, satin y algodon');

COMMIT;

-- Inserción de Productos (Ropa Interior y Bodys)
INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, imagen_url)
VALUES ('Body Encaje Velvet', 'Body delicado con copa prehormada y detalles en encaje', 55000.0, 12, (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Ropa Interior y Bodys'), 'asset/bodys.jpeg');

INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, imagen_url)
VALUES ('Cachetero Encaje Soft', 'Cachetero suave sin costuras visibles de alta comodidad', 22000.0, 25, (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Ropa Interior y Bodys'), 'asset/cachetero.jpeg');

INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, imagen_url)
VALUES ('Set Ropa Interior Glam', 'Conjunto de dos piezas en encaje fino ajustable', 48000.0, 10, (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Ropa Interior y Bodys'), 'asset/set de ropa interior.jpeg');

INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, imagen_url)
VALUES ('Top Básico Confort', 'Top de descanso con soporte ligero en tela transpirable', 32000.0, 18, (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Ropa Interior y Bodys'), 'asset/top.jpeg');

-- Inserción de Productos (Pijamas)
INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, imagen_url)
VALUES ('Pijama Satín Clásica', 'Conjunto de camisa manga larga y pantalón en satín brillante', 75000.0, 15, (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Pijamas'), 'asset/pijama.jpeg');

INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, imagen_url)
VALUES ('Pijama Cute Algodón', 'Pijama de short y blusa fresca en 100% algodón suave', 62000.0, 20, (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Pijamas'), 'asset/pijama cute.jpeg');

INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, imagen_url)
VALUES ('Pijama Pasión Seda', 'Conjunto premium de descanso con acabados elegantes en seda', 80000.0, 8, (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Pijamas'), 'asset/pijama pasion.jpeg');

INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, imagen_url)
VALUES ('Combo Set Descanso', 'Set completo de 3 piezas: bata ligera, blusa y pantalón', 89000.0, 10, (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Pijamas'), 'asset/combo set.jpeg');

COMMIT;