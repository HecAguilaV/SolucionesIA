# 🧪 Batería de Pruebas — Agente Conversacional ALI

Este documento contiene un conjunto estructurado de escenarios y preguntas de prueba para validar el comportamiento del **Agente de Logística Inteligente (ALI)**.

---

## 1. Escenarios de Consulta de Inventario y Memoria (Conversación en Hilo)

Para evaluar el correcto funcionamiento de las herramientas de consulta y la **memoria de ventana de corto plazo (k=10)**, realiza las siguientes preguntas de forma secuencial en una misma conversación:

*   **Paso 1 (Contexto Inicial):**
    > *"¿Cuál es el stock actual del bloqueador solar (**SKU-1001**) en la sucursal de Viña del Mar?"*
    *   *Resultado esperado:* El agente llama a la herramienta `consultar_inventario` y responde que hay un stock físico de **8 unidades** (crítico).
*   **Paso 2 (Referencia Implícita):**
    > *"¿Cuál ha sido su promedio de ventas diarias en los últimos 30 días?"*
    *   *Resultado esperado:* La memoria asocia "su" al bloqueador solar anterior. El agente llama a `analizar_tendencias` para el `SKU-1001` y calcula la venta promedio diaria (aproximadamente 20 unidades/día).
*   **Paso 3 (Análisis y Cálculo de Reorden):**
    > *"Según las políticas de OmniRetail, ¿cuál es el Punto de Reorden (ROP) para este bloqueador solar y cuándo deberíamos pedir reposición?"*
    *   *Resultado esperado:* El agente llama a `buscar_politicas_empresa` (RAG), recupera la fórmula `ROP = (Venta Promedio * Lead Time) + Stock Seguridad` e indica que con 8 unidades estamos muy por debajo del ROP (que es ~100 unidades), catalogándolo como **Crítico**.

---

## 2. Escenarios RAG (Políticas de Negocio de OmniRetail)

Prueba que el agente recupere documentos precisos de ChromaDB sin inventar información:

*   **Pregunta RAG 1 (Stock de Seguridad):**
    > *"¿Cuáles son los niveles de stock de seguridad obligatorios que define la empresa según la categoría de producto?"*
*   **Pregunta RAG 2 (Alertas Meteorológicas):**
    > *"¿Qué reglas de abastecimiento especial se aplican a los productos estacionales si hay una alerta de ola de calor o tormenta?"*
*   **Pregunta RAG 3 (Puntos de Reorden):**
    > *"¿Cómo se calcula el punto de reorden (ROP) y qué acción automática se debe tomar según el manual?"*

---

## 3. Escenarios de Planificación Dinámica (Novedad v2)

Valida que el agente active las distintas estrategias de planificación según tus palabras clave:

*   **Planificación Jerárquica (Nivel Estratégico, Análisis y Operación):**
    > *"Realizá una **planificación jerárquica** de reposición para el producto estacional de invierno **SKU-1004** en Concepción."*
*   **Planificación Reactiva (Evaluación basada en reglas del entorno):**
    > *"Ejecuta un análisis **reactivo** ya que tenemos una alerta de stock crítico en la tienda de Santiago."*
*   **Planificación por Objetivos (Secuencia lineal orientada a metas):**
    > *"**Planifica** una propuesta de compras formal para reponer los bloqueadores solares de Viña del Mar y escribe un reporte con la recomendación."*

---

## 4. Escenarios Offline (Contingencia SQL)

Para probar este flujo, debes apagar internet o dejar vacías las API keys del archivo `.env`. El agente activará su motor local.

> [!WARNING]
> En este modo, el agente solo responde a consultas con palabras clave de inventario (**"stock"**, **"inventario"**, **"bajo"**).

*   **Pregunta local válida:**
    > *"Mostrame el inventario bajo o crítico"*
    *   *Resultado esperado:* Te devolverá la lista formateada extraída directamente de SQLite con los productos con stock inferior o igual a 10.
*   **Pregunta local fuera de límite:**
    > *"¿Cuál es la política de la empresa?"*
    *   *Resultado esperado:* Te indicará que el modo de contingencia local está activo y que no puede acceder a las políticas de negocio en este momento.
