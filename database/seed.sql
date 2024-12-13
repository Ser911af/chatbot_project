-- Insertar los datos en la tabla ventas
INSERT INTO ventas (fecha, cliente, monto, metodo_pago, descripcion) VALUES
('2024-11-01', 'Cliente A', 1500.00, 'Tarjeta', 'Venta de servicios X'),
('2024-11-15', 'Cliente B', 2000.00, 'Transferencia', 'Venta de productos Y'),
('2024-12-05', 'Cliente A', 1800.00, 'Efectivo', 'Venta de servicios Z');

-- Insertar los datos en la tabla cuentas_por_pagar
INSERT INTO cuentas_por_pagar (cliente, saldo, fecha_vencimiento, estado) VALUES
('Cliente A', 500.00, '2024-12-20', 'Pendiente'),
('Cliente B', 1000.00, '2025-01-15', 'Pendiente'),
('Cliente C', 0.00, NULL, 'Pagado');

-- Insertar los datos en la tabla balances_financieros
INSERT INTO balances_financieros (año, ingresos_totales, egresos_totales, beneficio_neto) VALUES
(2023, 50000.00, 30000.00, 20000.00),
(2024, 60000.00, 40000.00, 20000.00);