-- Crear tabla de ventas
CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    cliente VARCHAR(255) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    metodo_pago VARCHAR(50),
    descripcion TEXT
);


-- Crear tabla de cuentas por pagar
CREATE TABLE cuentas_por_pagar (
    id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente VARCHAR(255) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL,
    fecha_vencimiento DATE,
    estado VARCHAR(50) DEFAULT 'Pendiente'
);



-- Crear tabla de balances financieros
CREATE TABLE balances_financieros (
    id_balance INTEGER PRIMARY KEY AUTOINCREMENT,
    año INTEGER NOT NULL,
    ingresos_totales DECIMAL(10, 2),
    egresos_totales DECIMAL(10, 2),
    beneficio_neto DECIMAL(10, 2)
);






