-- 1. Consultar todos los productos con el nombre de su categoría (para el catálogo)
SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen_url, c.nombre_categoria
FROM productos p
JOIN categorias c ON p.id_categoria = c.id_categoria
ORDER BY p.id_producto;

-- 2. Indicadores (Dashboard)
SELECT 
    (SELECT COUNT(*) FROM productos) AS total_productos,
    (SELECT COUNT(*) FROM pedidos) AS total_pedidos,
    (SELECT NVL(SUM(total), 0) FROM pedidos) AS total_ventas
FROM dual;

-- 3. Consultar historial de pedidos de un usuario con su detalle
SELECT pe.id_pedido, pe.fecha_pedido, pe.total, pe.estado, pr.nombre AS producto, dp.cantidad, dp.precio_unitario
FROM pedidos pe
JOIN detalles_pedido dp ON pe.id_pedido = dp.id_pedido
JOIN productos pr ON dp.id_producto = pr.id_producto
WHERE pe.id_usuario = 2
ORDER BY pe.fecha_pedido DESC;
