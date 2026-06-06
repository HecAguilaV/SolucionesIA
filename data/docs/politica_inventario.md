# Política de Gestión de Inventario - OmniRetail S.A.

## 1. Niveles de Stock de Seguridad
Para mitigar riesgos de quiebres de stock, OmniRetail establece los siguientes niveles de stock de seguridad obligatorios, basados en la categoría del producto:

*   **Productos Perecederos (Alimentos frescos):** Stock de seguridad de 2 días de venta promedio.
*   **Productos Estacionales (Verano/Invierno):** Stock de seguridad del 20% sobre la proyección de ventas para el mes en curso. Si hay alertas climáticas (ej. ola de calor), el stock de seguridad debe aumentar un 15% adicional.
*   **Electrónica y Electrodomésticos:** Stock de seguridad equivalente a 1 semana de venta promedio.
*   **Productos de Alta Rotación (Básicos/Limpieza):** Stock de seguridad equivalente a 2 semanas de venta promedio.

## 2. Puntos de Reorden (ROP)
El punto de reorden determina cuándo debe emitirse una nueva orden de compra al proveedor.
*   **Cálculo Estándar:** ROP = (Venta Diaria Promedio * Lead Time del Proveedor) + Stock de Seguridad.
*   **Regla de Acción:** Siempre que el inventario físico caiga por debajo del ROP, se debe generar automáticamente una sugerencia de reposición.

## 3. Cantidad Económica de Pedido (EOQ)
Aunque las sugerencias base utilicen ROP, el Agente de Inventario debe buscar optimizar los costos de pedido y almacenamiento.
*   Los pedidos de **Electrónica** no deben superar las 50 unidades por orden debido al alto costo de almacenamiento y seguros.
*   Los pedidos de **Alimentos no perecederos** deben redondearse al múltiplo de 100 más cercano para aprovechar descuentos por volumen de pallet.

## 4. Alertas de Quiebre
Cualquier producto cuyo stock actual sea igual o menor al 50% de su stock de seguridad debe ser marcado como **CRÍTICO** y requiere reposición acelerada (express), sin importar el costo de envío adicional.
