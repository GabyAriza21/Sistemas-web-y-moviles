-- Verificación de llaves y restricciones creadas en las tablas
SELECT table_name, constraint_name, constraint_type, status
FROM user_constraints
WHERE table_name IN ('ROLES', 'USUARIOS', 'CATEGORIAS', 'PRODUCTOS', 'PEDIDOS', 'DETALLES_PEDIDO')
ORDER BY table_name;
