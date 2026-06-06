# LearningIA — Chuleta Técnica de ALI (Agente de Logística Inteligente)

¡Bienvenido a la guía de referencia rápida de **ALI**! Este documento está diseñado para ayudarte a entender la arquitectura, el funcionamiento del sistema RAG, la base de datos SQL y cómo probar cada funcionalidad.

---

## 🗺️ Mapa de Archivos Clave del Proyecto
Para navegar rápido, acá tenés los accesos directos a los componentes clave del sistema:

*   **Configuración y Arranque:**
    *   [start.sh](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/start.sh) — Script de inicio automático (Backend + Frontend + Kernel Jupyter).
    *   [README.md](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/README.md) — Instrucciones generales de instalación y ejecución.
    *   [.env](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/.env) — Variables de entorno (claves API de GitHub o Google).
    *   [requirements.txt](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/requirements.txt) — Dependencias de Python del proyecto.

*   **Base de Datos y Scripts de Carga:**
    *   [scripts/setup_db.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/scripts/setup_db.py) — Script para inicializar la base de datos SQLite y generar ventas históricas sintéticas.
    *   [scripts/ingest_docs.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/scripts/ingest_docs.py) — Script para fragmentar (chunking) y cargar las políticas en ChromaDB (RAG).
    *   [data/omniretail.db](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/data/omniretail.db) — Archivo físico de la base de datos SQLite.
    *   [data/chroma_store/](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/data/chroma_store/) — Directorio de la base de datos vectorial de Chroma.

*   **Capa del Backend (FastAPI):**
    *   [backend/main.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/main.py) — Servidor API FastAPI que expone los endpoints dinámicos (`/api/health`, `/api/inventory/critical`, `/api/agent/chat`).
    *   [backend/src/application/agent.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/application/agent.py) — Lógica de orquestación de ALI utilizando LangChain.
    *   [backend/src/infrastructure/vector_store.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/infrastructure/vector_store.py) — Adaptador que conecta a ChromaDB y realiza búsquedas de similitud (RAG).
    *   [backend/src/infrastructure/database.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/infrastructure/database.py) — Adaptador para las consultas SQL sobre SQLite.
    *   [backend/src/infrastructure/llm_provider.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/infrastructure/llm_provider.py) — Gestor de modelos con triple fallback (GitHub Models -> Google Gemini -> Local Mock).

*   **Herramientas (Tools) Autónomas de ALI:**
    *   [backend/src/tools/inventory_query.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/inventory_query.py) — Herramienta para consultar stock en la DB.
    *   [backend/src/tools/trend_analyzer.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/trend_analyzer.py) — Herramienta para analizar promedios de ventas históricas.
    *   [backend/src/tools/weather_checker.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/weather_checker.py) — Herramienta para verificar condiciones del clima.
    *   [backend/src/tools/recommendation_engine.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/recommendation_engine.py) — Herramienta para invocar al RAG de ChromaDB.
    *   [backend/src/tools/report_writer.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/report_writer.py) — Herramienta para guardar reportes en el disco local.

*   **Capa del Frontend (React + Vite):**
    *   [frontend/src/App.jsx](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/frontend/src/App.jsx) — Interfaz principal moderna con panel de métricas y chat.
    *   [frontend/src/index.css](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/frontend/src/index.css) — Sistema de diseño visual premium (Light Slate & Emerald Theme).
    *   [frontend/src/components/AgentChat.jsx](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/frontend/src/components/AgentChat.jsx) — Componente de chat con renderizado estructurado para JSON y Markdown.
    *   [frontend/src/components/KPICards.jsx](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/frontend/src/components/KPICards.jsx) — Tarjetas indicadoras de inventario, bodegas y estado de la API.

---

## 🧠 ¿Qué es RAG (Retrieval-Augmented Generation) y cómo funciona acá?

### Concepto Básico
Un LLM común sabe muchas cosas del mundo, pero **no tiene idea de las reglas de tu negocio** (por ejemplo, qué hacer si hay una alerta de lluvia en Concepción y el bloqueador solar está con bajo stock). 

**RAG** soluciona esto en tres pasos:
1.  **Recuperación (Retrieve):** Cuando le preguntás a ALI sobre una política, el sistema busca los documentos de texto más relevantes en una base de datos especial.
2.  **Aumentación (Augment):** Esos documentos se añaden ("inyectan") directamente al prompt que se le envía al LLM.
3.  **Generación (Generate):** El LLM lee el prompt con las políticas agregadas y genera una respuesta informada, precisa y basada en las reglas reales de la empresa, evitando inventar (alucinar) información.

### ¿Dónde está y cómo se ejecuta el RAG en este proyecto?
*   **Archivos de origen:** Las políticas de la empresa están en archivos Markdown dentro de [data/docs/](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/data/docs/). Por ejemplo:
    *   [data/docs/politica_inventario.md](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/data/docs/politica_inventario.md) — Reglas de stock de seguridad por categoría.
    *   [data/docs/guia_reposicion.md](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/data/docs/guia_reposicion.md) — Qué hacer ante alertas meteorológicas estacionales.
*   **La Base de Datos Vectorial:** Usamos **ChromaDB**, que almacena los textos transformados en vectores. Esta base de datos se guarda físicamente en el directorio [data/chroma_store/](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/data/chroma_store/).
*   **¿Cómo se ejecuta el proceso de carga?**
    Ejecutamos el script de ingesta:
    ```bash
    PYTHONPATH=. python scripts/ingest_docs.py
    ```
    Este script toma las secciones de los archivos Markdown, genera sus representaciones vectoriales con el modelo `SentenceTransformer('all-MiniLM-L6-v2')` (generando 7 fragmentos en total provenientes de los encabezados `## `) y las guarda en ChromaDB.

---

## 🧪 Batería de Pruebas: Preguntas para ALI

Dependiendo de si las APIs (GitHub o Gemini) están activas o si estamos operando en modo local desconectado, podés hacer las siguientes pruebas:

### 🟢 Caso A: Agente Online (Con LLM / API activa)
El agente utiliza todo su potencial: puede razonar, planificar, encadenar llamadas a múltiples herramientas (ReAct) y consultar ChromaDB.

1.  **Preguntas de Políticas Corporativas (RAG):**
    *   *"¿Cuál es la política de la empresa sobre el nivel de stock de seguridad para productos perecederos?"*
    *   *"¿Qué debemos hacer si el inventario de un producto baja de su punto de reorden (ROP)?"*
    *   *"¿Cómo afecta una tormenta eléctrica al lead time de los proveedores según las normas?"*
2.  **Consultas Cruzadas Inteligentes (Clima + Inventario + Ventas + RAG):**
    *   *"Se pronostica lluvia en Concepción. ¿Tenemos stock suficiente de paraguas según las políticas de reposición ante factores climáticos?"*
    *   *"Hay una ola de calor proyectada en Viña del Mar (> 30°C). Analizá si el stock de bloqueadores solares es suficiente y calcula si debemos pedir más."*
3.  **Generación de Reportes Guardados:**
    *   *"Haz un análisis completo del stock de la bebida isotónica en Santiago, evalúa las tendencias de venta y escribe un reporte formal con recomendaciones."*

---

### 🔴 Caso B: Agente Offline (APIs "Muertas" / Sin Tokens)
Si las API keys son inválidas o no hay internet, ALI activa de forma automática el **Fallback SQL Offline**. Este modo no puede razonar con LLMs ni consultar ChromaDB, pero tiene una heurística de emergencia que interroga directamente a la base de datos SQLite.

Para obtener respuestas en este modo, debes usar palabras clave como **"stock"**, **"inventario"** o **"bajo"** en tu pregunta:

1.  **Preguntas Heurísticas que Responderá con Éxito:**
    *   *"¿Cuáles son los productos con stock bajo?"*
    *   *"Mostrame el inventario crítico actual."*
    *   *"Decime qué productos están bajo el límite."*
    
    *(En este caso, la base de datos devolverá una lista real y formateada de los productos con stock inferior o igual a 10 extraída dinámicamente de SQLite).*
2.  **Preguntas Fuera de la Heurística de Emergencia:**
    *   *"¿Qué temperatura hace en Concepción?"*
    *   *"¿Cuál es el descuento por volumen de alimentos?"*
    
    *(Cualquier pregunta que no contenga los términos clave recibirá un mensaje estandarizado indicando que las APIs están caídas y que solo puede responder sobre stock crítico en este momento).*

---

## 📐 Metodología: ¿SDD o TDD?

En este proyecto conviven ambas aproximaciones en armonía:

1.  **SDD (Spec-Driven Development) para la Arquitectura y Lógica del Agente:**
    Se utiliza para diseñar el comportamiento del agente. Escribimos especificaciones exactas (como las metas descritas en [implementation_plan.md](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/openspec/changes/arquitectura-empresarial/implementation_plan.md)) antes de escribir código, asegurando que las herramientas (tools) y la memoria del agente encajen perfectamente en la Clean Architecture.
2.  **TDD (Test-Driven Development) para las Herramientas e Infraestructura:**
    Se utiliza para garantizar la robustez técnica. Los adaptadores de bases de datos ([database.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/infrastructure/database.py)) y vectoriales ([vector_store.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/infrastructure/vector_store.py)) tienen suites de pruebas automatizadas en `tests/` para verificar su correcto funcionamiento matemático y lógico, previniendo regresiones en producción.
