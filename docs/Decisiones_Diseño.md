# Decisiones de Diseño y Arquitectura

Este documento justifica las decisiones técnicas tomadas para la construcción del Agente de Gestión de Inventario OmniRetail, basándose en los requerimientos del curso (ISY0101).

## 1. Patrón Arquitectónico: Clean Architecture

Se decidió implementar Clean Architecture (propuesta por Uncle Bob) en lugar de un script monolítico de Python.

**Justificación:**
Un agente inteligente en un entorno corporativo debe poder evolucionar. Al separar las entidades de dominio (`Product`, `InventoryStatus`) de la lógica del agente (`AgentExecutor`) y de la infraestructura (`TripleFallbackLLMProvider`, `ChromaDBVectorStoreAdapter`), garantizamos que:

- El LLM puede ser cambiado sin reescribir la lógica de negocio.
- Las herramientas (`@tool`) son independientes de cómo se orquesta la memoria.
- Permite la inclusión de tests unitarios aislados.

## 2. Orquestador: LangChain vs CrewAI

**Decisión:** Uso de LangChain nativo (`AgentExecutor`) en lugar de CrewAI.

**Justificación:**
Como se evidenció en los materiales de clase (IL2.1), CrewAI brilla en entornos donde múltiples roles deben interactuar entre sí secuencial u jerárquicamente (ej. un Analista, un Escritor, un Revisor).
Para el caso de OmniRetail, el caso de uso requiere de un **único agente con gran capacidad de razonamiento** y acceso a múltiples herramientas para ejecutar una tarea compleja de una sola vez. Añadir CrewAI agregaría "overhead" y complejidad innecesaria para la estructura actual, aunque la arquitectura limpia permite escalar hacia un equipo multi-agente si los requerimientos cambian.

## 3. Proveedor LLM: Triple Fallback

**Decisión:** Se implementó una cascada de provisión: GitHub Models (primario) -> Google Gemini (secundario) -> Offline SQL (fallback de emergencia).

**Justificación:**
Las API públicas (especialmente en cuentas de estudiantes o gratuitas) tienen límites de cuota (rate limits) estrictos. En una demostración en vivo, un error 429 es catastrófico. Implementar un fallback múltiple demuestra robustez arquitectónica y tolerancia a fallos. El fallback offline basado en SQLite asegura que el sistema nunca "caiga" y pueda brindar soporte vital en todo momento.

## 4. Memoria

**Decisión:** Uso combinado de `ConversationBufferWindowMemory` y `ChromaDB` (RAG).

**Justificación:**

- **Window Memory:** Garantiza que el agente mantenga el contexto de la sesión actual sin desbordar la ventana de tokens (limita a las últimas 10 interacciones).
- **RAG (SemanticRetriever):** Las políticas de la empresa no deben depender de la alucinación del modelo. Almacenar documentos en ChromaDB permite inyectar reglas duras de negocio precisas ("grounding") antes de tomar decisiones.

## 5. UI: Streamlit

**Decisión:** Frontend con Streamlit en lugar de CLI.

**Justificación:**
Emula el entorno corporativo real de un jefe de tienda o de logística, proporcionando visibilidad inmediata sobre estados críticos (ej. productos con stock <= 10) fuera del chat, pero interactuando de manera conversacional para tareas profundas.
