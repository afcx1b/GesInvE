CREATE VIEW registrarInventarioInicial AS
SELECT 
    i.id AS inventario_id,
    k.id AS kardex_id,
    c.id AS costo_id,
    i.fecha_registro,
    i.cantidad,
    i.producto_id,
    k.cantidad AS kardex_cantidad,
    c.costo_unitario
FROM 
    Inventario i
JOIN 
    Kardex k ON i.producto_id = k.producto_id
JOIN 
    Costo c ON i.producto_id = c.producto_id
WHERE 
    i.tipo_movimiento = 'INICIAL';
