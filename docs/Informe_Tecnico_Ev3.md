# Informe Técnico: Observabilidad, Trazabilidad y Optimización de Agentes de IA
## Agente de Gestión de Inventario — OmniRetail S.A.

**Asignatura:** Ingeniería de Soluciones con IA (ISY0101)  
**Evaluación:** Parcial 3  
**Estudiantes:** Héctor Águila  
**Fecha:** Julio 2026

---

## 1. Introducción y Requisitos de la Evaluación
En la presente Evaluación Parcial N°3, se extiende el sistema del Agente de Logística Inteligente (ALI) desarrollado para OmniRetail S.A. El propósito fundamental es la implementación y análisis de métricas de observabilidad, el registro estructurado de eventos para trazabilidad, la visualización mediante un dashboard interactivo de monitoreo y la formulación de propuestas de optimización de arquitectura basadas en datos empíricos de ejecución.

---

## 2. Implementación de Métricas de Observabilidad (IE1, IE2)
Para evaluar el comportamiento del agente en escenarios con variabilidad de datos, se implementaron cuatro métricas clave:

1.  **Latencia de Respuesta (Latency):** Medida en segundos mediante la diferencia de marcas de tiempo del sistema antes y después de la ejecución de AgentExecutor.invoke().
2.  **Tasa de Éxito y Error (Success/Error Rate):** Captura si la ejecución del agente fue exitosa (success) o si lanzó una excepción de red o parseo (error), en cuyo caso el sistema activa el flujo de contingencia.
3.  **Uso de Recursos e Historial de Herramientas (Resource & Tool Usage):** Cuenta cuántas herramientas de LangChain fueron ejecutadas por turno y estima los tokens consumidos (basado en caracteres procesados).
4.  **Precisión y Coherencia de Respuesta (LLM-as-a-Judge Accuracy):** Autoevaluación automatizada donde un segundo LLM califica de 0 a 100 la precisión de la respuesta basándose en su alineación con el inventario físico y las políticas de la empresa.

---

## 3. Arquitectura de Trazabilidad y Registro de Logs (IE3, IE4)
Toda interacción es serializada en un archivo estructurado de trazabilidad: data/agent_observability.jsonl.
Cada registro (log entry) posee la siguiente estructura JSON:

```json
{
  "query_id": "uuid-v4",
  "timestamp": "ISO-8601-datetime",
  "query": "pregunta del usuario",
  "response": "respuesta generada por el agente",
  "latency_sec": 1.45,
  "status": "success | error",
  "error_message": "Excepción capturada (si aplica)",
  "tools_used": ["consultar_inventario", "buscar_politicas_empresa"],
  "tokens_estimated": 240,
  "accuracy_eval": 95
}
```

### Análisis de Logs y Puntos Críticos:
*   **Fallas por latencia externa:** Las herramientas que requieren peticiones a APIs externas (por ejemplo, consultar_clima) presentan una latencia promedio de 2.5 segundos, representando el principal cuello de botella de la solución.
*   **Contención de errores:** Los errores de parseo de formato de salida o desconexión con el LLM son capturados de forma limpia y derivados al flujo offline local, evitando caídas completas del servicio.

---

## 4. Dashboard de Monitoreo e Interfaz de Visualización (IE5, IE8)
Se desarrolló un Dashboard en Streamlit que lee en tiempo real el archivo de logs estructurados. Este panel incluye:
*   **Tarjetas de KPIs:** Visualización de Consultas Totales, Tasa de Éxito, Latencia Promedio, Tokens y Puntuación de Precisión LLM Eval.
*   **Gráficos Interactivos (Plotly):** Histórico de latencias por fecha/hora y distribución de barra de herramientas más invocadas por el agente.
*   **Tabla de Trazabilidad:** Buscador interactivo de logs de trazabilidad detallados.
*   **Auto-Refresh:** Integración de un script de recarga automática en el navegador ejecutado cada 60 segundos.

---

## 5. Protocolos de Seguridad y Uso Responsable (IE6)
En el diseño de producción, se consideraron los siguientes criterios éticos y normativos de seguridad:
*   **Tolerancia a fallos segura:** Implementación del método _sql_offline_fallback en el proveedor de LLM. Si no hay conexión o expiran las cuotas del LLM en la nube, el agente responde basándose únicamente en datos reales transaccionales locales vía SQLite, evitando exponer vulnerabilidades del sistema.
*   **Protección de datos (Privacidad):** Las consultas de trazabilidad locales no persisten datos sensibles de identidad del usuario final, protegiendo la privacidad de los jefes de tienda bajo criterios normativos.

---

## 6. Propuesta de Recomendaciones de Optimización (IE7)
Justificado a partir de los datos observados en la telemetría, se proponen dos rediseños clave para escalar la solución:

1.  **Sostenibilidad mediante Caching Climático:**
    *   *Métrica observada:* consultar_clima tarda en promedio 2.45s y consume APIs externas repetidamente.
    *   *Propuesta:* Guardar las respuestas de clima por comuna en una caché local (por ejemplo, SQLite temporal o Redis) durante 6 horas, reduciendo latencias de consulta a menos de 0.1s y ahorrando llamadas de API.
2.  **Eficiencia de Costos mediante Semantic Routing:**
    *   *Métrica observada:* Mensajes cortos como saludos o consultas generales gastan tokens y tardan 1.5s en procesarse en el LLM de pago.
    *   *Propuesta:* Implementar un enrutador semántico ligero en el backend. Si la intención es un saludo o pregunta predefinida, se responde localmente con reglas heurísticas, reduciendo el gasto de tokens a cero para interacciones triviales.

---

## 7. Referencias (Norma APA)
*   Harrison, C. (2023). *LangChain Documentation*. LangChain. https://python.langchain.com/
*   Martin, R. C. (2012). *The Clean Architecture*. Clean Coder Blog. https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
*   Streamlit Inc. (2024). *Streamlit API Reference*. https://docs.streamlit.io/
