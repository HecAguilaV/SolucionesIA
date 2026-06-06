# Propuesta de Caso Organizacional: Evaluación Parcial N°1
## Proyecto: Soporte a Decisiones en Gestión de Inventario para Retail

### 1. Nombre y descripción de la organización
**Nombre:** OmniRetail S.A.
**Rubro:** Retail / Supermercados y Tiendas de Conveniencia.
**Descripción:** OmniRetail es una cadena de retail con presencia nacional que opera múltiples centros de distribución y cientos de puntos de venta. La organización maneja un catálogo de más de 10,000 SKUs y enfrenta una logística compleja debido a la variabilidad de la demanda estacional y regional.

### 2. Identificación y descripción del problema/desafío
OmniRetail enfrenta dos problemas críticos y opuestos en su cadena de suministro:
1.  **Rupturas de Stock (Out-of-Stock):** Incapacidad de satisfacer la demanda en momentos clave, lo que resulta en pérdida de ventas y disminución de la lealtad del cliente.
2.  **Sobrecostos de Almacenamiento:** Exceso de inventario en productos de baja rotación, lo que inmoviliza capital y genera costos elevados de bodegaje y riesgo de obsolescencia.

Actualmente, las decisiones de reposición se basan en métodos estadísticos tradicionales que no capturan eventos externos (clima, tendencias de redes sociales, feriados no lineales) ni permiten una explicación clara de *por qué* se recomienda una cantidad específica.

### 3. Objetivos de la intervención
-   **Objetivo General:** Desarrollar un agente inteligente basado en LLM y RAG que optimice la gestión de inventario mediante recomendaciones de pedidos justificadas.
-   **Objetivos Específicos:**
    -   Reducir las rupturas de stock en un 15% mediante el análisis de variables externas.
    -   Optimizar el espacio de almacén disminuyendo el sobrestock de productos estacionales.
    -   Proveer una interfaz conversacional para que los jefes de tienda comprendan el razonamiento detrás de cada sugerencia de pedido.

### 4. Datos disponibles o que se pueden obtener
-   **Datos Internos (Estructurados y No Estructurados):**
    -   Historial de ventas por SKU y local (últimos 3 años).
    -   Reportes de inventario en tiempo real.
    -   Órdenes de compra históricas y tiempos de entrega de proveedores (Lead Times).
    -   Manuales de políticas de inventario de la empresa (PDFs para el RAG).
-   **Fuentes Externas (Vía API o Scraping):**
    -   Pronósticos meteorológicos (afectan ventas de alimentos, ropa, calefacción).
    -   Calendario de feriados y eventos especiales (CyberDay, Fiestas Patrias).
    -   Tendencias de mercado extraídas de reportes sectoriales.

### 5. Restricciones o requerimientos particulares
-   **Integración ERP:** La solución debe ser compatible conceptualmente con sistemas SAP o Microsoft Dynamics.
-   **Explicabilidad:** El agente no solo debe dar un número, sino justificarlo (ej: "Se recomienda aumentar stock de bloqueador solar un 20% debido a la ola de calor pronosticada para el fin de semana").
-   **Privacidad:** Los datos de ventas deben ser anonimizados para no comprometer información sensible de clientes.

### 6. Motivación para el uso de agentes de IA, LLMs y RAG
El uso de **LLMs** permite interpretar variables cualitativas (tendencias, noticias) que los modelos puramente matemáticos ignoran. El pipeline **RAG** es fundamental para que el agente tenga acceso a la "memoria" de la empresa (históricos y manuales) sin necesidad de reentrenar el modelo constantemente. La arquitectura de **agentes** permite orquestar herramientas externas (APIs de clima) y sistemas internos (base de datos de ventas) de forma autónoma y coherente.

---
**Participantes:** [Nombres de los integrantes]
**Fecha:** 25 de abril de 2026
