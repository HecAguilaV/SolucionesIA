# Guía de Aprendizaje: Arquitectura y Estructura del Backend

Esta guía detalla el funcionamiento del Backend del Agente de Logística Inteligente (ALI), explicando la responsabilidad de cada carpeta y el propósito específico de cada uno de sus archivos bajo los principios de **Clean Architecture**.

---

## 1. Propósito General del Backend
El backend tiene como objetivo principal exponer una API REST (FastAPI) para interactuar con el agente conversacional, orquestar su ciclo de toma de decisiones (planificación y uso de herramientas), gestionar la memoria a corto y largo plazo del agente, y capturar métricas continuas de observabilidad y trazabilidad sobre cada ejecución.

---

## 2. Estructura de Carpetas del Backend (`backend/`)

La raíz del backend contiene los ejecutables principales, delegando la lógica de negocio a la carpeta modular `src/`:

*   **`main.py`:** Es el punto de entrada de la aplicación FastAPI. Expone los endpoints HTTP `/api/agent/chat` (para conversar con el agente) y `/api/metrics` (para recuperar la telemetría en JSON).
*   **`dashboard.py`:** Panel analítico interactivo desarrollado en Streamlit. Lee el archivo de logs de observabilidad y renderiza en vivo gráficos interactivos y KPIs de rendimiento.

---

## 3. Estructura de la Capa de Lógica (`backend/src/`)

Sigue las directrices de la arquitectura limpia, dividiendo las responsabilidades en capas desacopladas:

### 3.1. Capa de Dominio (`src/domain/`)
Contiene las entidades puras y las interfaces del sistema, completamente independientes de bases de datos o frameworks externos.
*   **`entities.py`:** Define las estructuras de datos (dataclasses de Python) que representan los conceptos de negocio: `Product`, `InventoryStatus` y `Sale`.
*   **`interfaces.py`:** Define las clases abstractas e interfaces (contratos de código) que deben implementar las bases de datos y proveedores de LLM.

### 3.2. Capa de Casos de Uso / Aplicación (`src/application/`)
Contiene las reglas de negocio específicas del flujo de la aplicación.
*   **`agent.py`:** Define la clase `InventoryAgent`. Configura el prompt de sistema del asistente de logística, inicializa las herramientas del agente y orquestal el ciclo ReAct (Reason + Act) usando LangChain.
*   **`planner.py`:** Implementa los planificadores del sistema (`GoalOrientedPlanner`, `HierarchicalPlanner`, `ReactivePlanner`). Permiten al agente descomponer solicitudes complejas en pasos lógicos antes de actuar.

### 3.3. Capa de Adaptadores e Infraestructura (`src/infrastructure/`)
Implementa las conexiones físicas hacia servicios externos, bases de datos y frameworks.
*   **`database.py`:** Implementa el adaptador de base de datos transaccional SQLite (`SQLiteDatabaseAdapter`). Realiza consultas directas de lectura y escritura para productos y stocks.
*   **`llm_provider.py`:** Implementa `TripleFallbackLLMProvider`. Orquesta la conexión resiliente de LLMs en cascada (GitHub Models -> Google Gemini -> Fallback offline SQL local).
*   **`observability.py`:** Implementa `ObservabilityManager`. Mide latencias, calcula tokens estimados, registra éxitos/errores, llama al LLM evaluador para obtener el score de precisión (LLM-as-a-Judge) y escribe la traza estructurada en `agent_observability.jsonl`.
*   **`vector_store.py`:** Implementa la base de datos vectorial ChromaDB para el motor RAG. Permite indexar y buscar documentos de políticas de la empresa utilizando embeddings semánticos.

### 3.4. Capa de Memoria (`src/memory/`)
Gestión del contexto conversacional e información histórica.
*   **`conversation_memory.py`:** Implementa la memoria a corto plazo del agente conversacional usando `ConversationBufferWindowMemory` de LangChain.
*   **`semantic_retriever.py`:** Maneja las búsquedas semánticas sobre las políticas ingestadas en la base de datos vectorial.

### 3.5. Capa de Herramientas del Agente (`src/tools/`)
Funciones de acción del agente ALI expuestas mediante el decorador `@tool` de LangChain.
*   **`inventory_query.py`:** Consulta el inventario físico y en tránsito. Acepta el parámetro `sku` de forma opcional (si se omite, retorna la lista completa de stock).
*   **`trend_analyzer.py`:** Calcula promedios históricos de ventas diarias para ayudar a predecir quiebres de stock.
*   **`weather_checker.py`:** Consulta APIs climáticas para anticipar aumentos de demanda estacional (como bloqueador solar con altas temperaturas).
*   **`recommendation_engine.py`:** Invoca búsquedas en la base de datos vectorial para recuperar las reglas corporativas aplicables a reabastecimientos.
*   **`report_writer.py`:** Permite al agente persistir recomendaciones estructuradas y justificadas en archivos Markdown en disco.

### 3.6. Configuración General (`src/config/`)
*   **`settings.py`:** Carga las variables de entorno (.env) y establece las constantes del sistema como rutas de bases de datos y carpetas de almacenamiento.
