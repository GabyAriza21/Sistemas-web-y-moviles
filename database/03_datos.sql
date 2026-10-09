-- Insercion de roles y categorias de pijamas y bodys

INSERT INTO roles (nombre_rol) VALUES ('Administrador');
INSERT INTO roles (nombre_rol) VALUES ('Cliente');

INSERT INTO categorias (nombre_categoria, descripcion) VALUES ('Ropa Interior y Bodys', 'Prendas intimas y bodys para mujer');

COMMIT;