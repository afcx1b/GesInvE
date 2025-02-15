CREATE VIEW registrarBajaArticulos AS
SELECT 
    i.id AS inventario_id,
    k.id AS kardex_id,
    i.fecha_registro,
    i.cantidad,
    i.producto_id,
    k.cantidad AS kardex_cantidad
FROM 
    Inventario i
JOIN 
    Kardex k ON i.producto_id = k.producto_id
WHERE 
    i.tipo_movimiento = 'BAJA';
