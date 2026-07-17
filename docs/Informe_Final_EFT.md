# Informe Técnico Final: Consolidación de Solución de Agente de IA y RAG (EFT)

## Agente de Gestión de Inventario — OmniRetail S.A.

**Asignatura:** Ingeniería de Soluciones con Inteligencia Artificial (ISY0101)
**Evaluación:** Examen Final Transversal (EFT)
**Estudiante:** Héctor Águila
**Fecha:** Julio 2026

---

## 1. Análisis del Caso Organizacional

### 1.1 Contexto de la Organización y Desafíos

<p style="text-align: justify;">OmniRetail S.A., gran cadena de comercio minorista chilena, enfrentaba pérdidas operativas significativas debido a dos problemas en la gestión de su inventario: quiebres de stock (especialmente críticos en productos con alta demanda estacional) y sobreinventario (que inmoviliza capital y eleva los costos de almacenamiento).</p>

<p style="text-align: justify;">Las decisiones se tomaban analizando manualmente planillas desconectadas (ventas históricas, inventario físico) y políticas en lenguaje natural (coberturas ideales, reglas de reposición). El desafío era diseñar una solución que automatice y asista a los jefes de tienda en sus decisiones de reabastecimiento en menos de 5 minutos, considerando factores externos como el clima, erradicando alucinaciones del modelo y garantizando consistencia ante caídas de red.</p>

---

## 2. Diseño de la Solución Basada en LLM y RAG

### 2.1 Formulación y Optimización de Prompts

<p style="text-align: justify;">Para garantizar la precisión de las respuestas del agente, se definió un prompt de sistema estructurado para el agente en [backend/src/application/agent.py](../backend/src/application/agent.py) que delimita sus fronteras de acción:</p>

<ul>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Role-prompting</strong>: Identifica al agente como "ALI" (Agente de Logística Inteligente).</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Context Bounding</strong>: Restringe las respuestas exclusivamente a la base de datos local SQLite y los fragmentos RAG. Si los datos no existen en el contexto, el agente debe responder: "No dispongo de esa información".</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Fórmulas Obligatorias</strong>: Exige aplicar de forma estricta las reglas logísticas corporativas (Punto de Reorden - ROP, y Cantidad Económica de Pedido - EOQ) recuperadas vía RAG.</li>
</ul>

### 2.2 Implementación de Pipelines RAG

<p style="text-align: justify;">El pipeline RAG para datos no estructurados de políticas corporativas está implementado en:</p>

<ul>
    <li style="text-align: justify; margin-bottom: 8px;">[backend/src/infrastructure/vector_store.py](../backend/src/infrastructure/vector_store.py): Fragmentación del manual <a href="../data/docs/politica_inventario.md">politica_inventario.md</a> y <a href="../data/docs/guia_reposicion.md">guia_reposicion.md</a> en bloques de 500 caracteres con un overlap de 50. Los embeddings son calculados de forma local con el modelo open-source <code>sentence-transformers/all-MiniLM-L6-v2</code> e indexados en una colección de ChromaDB persistida localmente.</li>
    <li style="text-align: justify; margin-bottom: 8px;">[backend/src/memory/semantic_retriever.py](../backend/src/memory/semantic_retriever.py): Realiza búsquedas por similitud de coseno en ChromaDB, recuperando los 3 fragmentos de políticas corporativas más relevantes para alimentar el contexto del LLM.</li>
</ul>

### 2.3 Diseño de la Arquitectura Completa

<p style="text-align: justify;">El sistema se diseña bajo los lineamientos de Clean Architecture, dividiendo las responsabilidades en capas desacopladas (Domain, Use Cases, Adapters, Infrastructure), detallado en la documentación de arquitectura [docs/Arquitectura.md](Arquitectura.md).</p>

```mermaid
graph TD
    subgraph UI ["Capa de Interfaz de Usuario"]
        React["React Web App (Puerto 19051)"]
        Streamlit["Streamlit Dashboard (Puerto 18052)"]
    end

    subgraph Backend ["Capa de Adaptadores y FastAPI (Puerto 18050)"]
        API["FastAPI App (backend/main.py)"]
        RAG["SemanticRetriever"]
        DB["SQLiteDatabaseAdapter"]
    end

    subgraph Core ["Capa de Casos de Uso y Agente"]
        Agent["InventoryAgent (LangChain AgentExecutor)"]
        Planner["GoalOrientedPlanner (Planificación)"]
    end

    subgraph Data ["Capa de Infraestructura e Información"]
        SQLite[(SQLite DB: omniretail.db)]
        Chroma[(ChromaDB: vector_store)]
        LLM["TripleFallbackLLMProvider (LLM / Offline)"]
    end

    React -->|HTTP /api/agent/chat| API
    Streamlit -->|Lectura en tiempo real| Log[(agent_observability.jsonl)]
    API -->|Orquesta ejecución| Agent
    Agent -->|Planifica pasos| Planner
    Agent -->|Consulta políticas| RAG
    Agent -->|Consulta transaccional| DB
    Agent -->|Genera lenguaje| LLM
    RAG -->|Similarity Search| Chroma
    DB -->|SQL Queries| SQLite
```

---

## 3. Desarrollo de Agente Funcional

### 3.1 Integración de Herramientas (Tools)

<p style="text-align: justify;">El agente expone cinco herramientas decoradas con `@tool` ubicadas en el directorio [backend/src/tools/](../backend/src/tools/):</p>

<ul>
    <li style="text-align: justify; margin-bottom: 8px;"><code>consultar_inventario</code> ([inventory_query.py](../backend/src/tools/inventory_query.py)): Consulta el stock físico actual y en tránsito en SQLite.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><code>analizar_tendencias</code> ([trend_analyzer.py](../backend/src/tools/trend_analyzer.py)): Obtiene ventas históricas acumuladas y promedios diarios en SQLite.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><code>consultar_clima</code> ([weather_checker.py](../backend/src/tools/weather_checker.py)): Consume la API externa de clima para variables de estacionalidad.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><code>buscar_politicas_empresa</code> (asociado a [semantic_retriever.py](../backend/src/memory/semantic_retriever.py)): Recupera reglas de negocio mediante ChromaDB.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><code>escribir_reporte</code> ([report_writer.py](../backend/src/tools/report_writer.py)): Guarda propuestas lógicas de reposición en archivos Markdown locales.</li>
</ul>

### 3.2 Configuración de Memoria

<p style="text-align: justify;">Se utiliza una memoria con ventana deslizante `ConversationBufferWindowMemory` (`k=10`) implementada en [backend/src/memory/conversation_memory.py](../backend/src/memory/conversation_memory.py), equilibrando la retención de contexto conversacional reciente con la eficiencia del prompt de entrada del modelo.</p>

### 3.3 Planificación y Toma de Decisiones

<p style="text-align: justify;">El módulo [backend/src/application/planner.py](../backend/src/application/planner.py) define tres estrategias de planificación dinámica que evitan la improvisación del agente ante consultas complejas:</p>

<ul>
    <li style="text-align: justify; margin-bottom: 8px;"><code>GoalOrientedPlanner</code>: Define secuencias ordenadas de pasos para alcanzar metas (Ej: Analizar inventario -> Clima -> Políticas RAG -> Reporte).</li>
    <li style="text-align: justify; margin-bottom: 8px;"><code>HierarchicalPlanner</code>: Descompone consultas estratégicas abstractas en niveles (Estratégico, Análisis, Operativo).</li>
    <li style="text-align: justify; margin-bottom: 8px;"><code>ReactivePlanner</code>: Evalúa de forma inmediata reglas del entorno ante alertas críticas de stock o clima.</li>
</ul>

---

## 4. Implementación de Observabilidad, Trazabilidad y Seguridad

### 4.1 Métricas de Observabilidad y Justificación de Negocio

<p style="text-align: justify;">Para que el agente de logística sea viable en un entorno real de producción, se diseñó un manager de telemetría en [backend/src/infrastructure/observability.py](../backend/src/infrastructure/observability.py) que captura cuatro métricas clave por cada turno de conversación, guardando las trazas estructuradas en el archivo [data/agent_observability.jsonl](../data/agent_observability.jsonl):</p>

<ol>
    <li style="text-align: justify; margin-bottom: 12px;"><strong>Latencia de Respuesta (Segundos)</strong>:
        <p style="text-align: justify; margin-top: 4px;"><em>Justificación</em>: En el comercio minorista, la velocidad operativa es crítica. Un agente logístico que tarda más de 30 segundos en responder causa frustración y provoca que los jefes de local abandonen la herramienta para volver a métodos manuales. El monitoreo de latencia permite identificar qué APIs externas (como el clima) representan cuellos de botella para el negocio.</p>
    </li>
    <li style="text-align: justify; margin-bottom: 12px;"><strong>Tasa de Errores (Éxitos / Fallas)</strong>:
        <p style="text-align: justify; margin-top: 4px;"><em>Justificación</em>: Mide la fiabilidad del agente. Un fallo en el sistema conversacional puede impedir la generación de una orden de reposición de emergencia, provocando quiebres de stock físicos.</p>
    </li>
    <li style="text-align: justify; margin-bottom: 12px;"><strong>Consumo de Recursos (Tokens y Herramientas Usadas)</strong>:
        <p style="text-align: justify; margin-top: 4px;"><em>Justificación</em>: El uso ineficiente de tokens en APIs pagadas de LLM eleva significativamente los costos operacionales cuando la solución se escala a nivel nacional. Monitorear los tokens consumidos y las herramientas invocadas permite ajustar el tamaño de la memoria de conversación y evaluar el ROI financiero del sistema.</p>
    </li>
    <li style="text-align: justify; margin-bottom: 12px;"><strong>Precisión (LLM-as-a-Judge)</strong>:
        <p style="text-align: justify; margin-top: 4px;"><em>Justificación</em>: En logística, un error de cálculo se traduce en dinero inmovilizado (sobreinventario) o pérdidas comerciales (desabastecimiento). El evaluador Juez (Gemini) contrasta en tiempo real la respuesta final del agente contra la base de datos relacional y las fórmulas corporativas del RAG, otorgando una calificación de precisión de 0 a 100 e identificando alucinaciones de forma automática.</p>
    </li>
</ol>

### 4.2 Trazabilidad de Logs y Análisis de Datos

<p style="text-align: justify;">Los logs son leídos y consolidados en tiempo real por el dashboard implementado en [backend/dashboard.py](../backend/dashboard.py).</p>

<ul>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Hallazgo clave</strong>: Los datos de observabilidad evidenciaron que la API externa del clima representaba el 60% de la latencia total del agente (promedio de 2.5 segundos de retraso por llamada).</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Propuesta de Rediseño</strong>: Diseñar un almacenamiento en caché local de 6 horas para el clima, y un módulo local de enrutamiento semántico (Semantic Routing) para responder interacciones cotidianas sin consumir llamadas de LLM externas.</li>
</ul>

### 4.3 Propuestas de Experimentos Futuros

<p style="text-align: justify;">Para consolidar la mejora del sistema, se proponen tres experimentos técnicos estructurados:</p>

<ul>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Experimento de Enrutamiento Semántico</strong>: Medir la variación en la latencia promedio y en el costo financiero (tokens consumidos) en una prueba A/B, implementando un enrutador semántico local vs. el agente ReAct tradicional para responder saludos y consultas triviales.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Experimento de Impacto de Caché</strong>: Evaluar la degradación de latencia del agente comparando el procesamiento de consultas de stock estacional con llamadas API directas de clima vs. consultas a caché SQLite local.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Prueba de Límite de Ventana de Memoria ($k$)</strong>: Evaluar la precisión (vía LLM-as-a-Judge) y el consumo de tokens incrementando la ventana de memoria de conversación ($k=5$, $k=10$, $k=20$, $k=30$) para identificar el punto óptimo de estabilidad conversacional.</li>
</ul>

### 4.4 Protocolos de Seguridad y Resiliencia Offline

<ul>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Modo Offline Fallback</strong>: Si las conexiones a internet fallan o las cuotas de API del LLM se agotan, la clase <code>TripleFallbackLLMProvider</code> en [backend/src/infrastructure/llm_provider.py](../backend/src/infrastructure/llm_provider.py) captura el error y activa de forma automática un motor heurístico local. Este motor procesa la consulta directamente contra la base SQLite y genera una lista de alertas logísticas en formato estructurado, manteniendo la continuidad operativa en la bodega sin conexión a red externa.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Privacidad</strong>: No se registran datos personales ni credenciales del personal en los archivos locales de logs, garantizando la soberanía de la información corporativa.</li>
</ul>

---

## 5. Mapeo Completo del Repositorio de la Solución

<p style="text-align: justify;">A continuación se detalla la función de cada archivo y componente del proyecto semestral:</p>

### 5.1 Capa de backend y Código Fuente (`backend/`)

* [backend/main.py](../backend/main.py): Orquestador e inicializador de la API FastAPI. Define las rutas HTTP `/api/agent/chat` que interactúan con la aplicación web.
* [backend/dashboard.py](../backend/dashboard.py): Panel de control interactivo desarrollado en Streamlit que lee las trazas del archivo de observabilidad y genera gráficos analíticos usando Plotly.
* [backend/src/application/agent.py](../backend/src/application/agent.py): Contiene la clase `InventoryAgent` encargada de armar el prompt, configurar las herramientas de LangChain y ejecutar la cadena ReAct.
* [backend/src/application/planner.py](../backend/src/application/planner.py): Define las tres clases planificadoras (`GoalOrientedPlanner`, `HierarchicalPlanner` y `ReactivePlanner`) para la descomposición lógica de metas.
* [backend/src/infrastructure/database.py](../backend/src/infrastructure/database.py): Implementa `SQLiteDatabaseAdapter` para encapsular las consultas de stock, ventas e inventario crítico.
* [backend/src/infrastructure/llm_provider.py](../backend/src/infrastructure/llm_provider.py): Implementa `TripleFallbackLLMProvider` para asegurar la resiliencia offline.
* [backend/src/infrastructure/vector_store.py](../backend/src/infrastructure/vector_store.py): Encargado del cliente local de ChromaDB, indexación de manuales y codificación de embeddings.
* [backend/src/memory/semantic_retriever.py](../backend/src/memory/semantic_retriever.py): Lógica de búsqueda por similitud de coseno del RAG.
* [backend/src/memory/conversation_memory.py](../backend/src/memory/conversation_memory.py): Adaptador de la memoria conversacional de LangChain.

### 5.2 Capa de Pruebas Unitarias (`tests/`)

* [tests/test_observability.py](../tests/test_observability.py): Pruebas automatizadas del manager de observabilidad. Asegura que los logs se guarden en JSON Lines, registren latencia y que la llamada al Juez no falle.
* [tests/test_planners.py](../tests/test_planners.py): Pruebas de integración que validan que los planificadores de lógica de negocio descompongan correctamente las consultas en secuencias esperadas de herramientas.

### 5.3 Carpeta de Documentación Técnica (`docs/`)

* [docs/Arquitectura.md](Arquitectura.md): Justifica la separación en capas de la solución y detalla el flujo de datos.
* [docs/Bateria_Pruebas.md](Bateria_Pruebas.md): Listado de escenarios y consultas preparadas para validación de RAG, memoria y offline fallback.
* [docs/Decisiones_Diseño.md](Decisiones_Diseño.md): Documento explicativo sobre la elección de patrones y frameworks lógicos (Clean Architecture, LangChain).

---

## 6. Conclusiones, Reflexiones y Declaración de Uso de IA

### 6.1 Conclusiones del Proyecto Semestral

<p style="text-align: justify;">La evolución de la solución a lo largo del semestre permitió contrastar los paradigmas de desarrollo tradicionales con el diseño basado en agentes inteligentes. La integración de Clean Architecture con técnicas de RAG local sobre ChromaDB demuestra ser la respuesta más estable para mitigar las alucinaciones en un entorno de negocios. La suite de observabilidad implementada no solo provee control operacional, sino que aporta la telemetría necesaria para fundamentar el rediseño y la optimización continua de la infraestructura.</p>

### 6.2 Reflexión Personal del Estudiante (Requisito Individual Obligatorio)

<p style="text-align: justify;">Durante el desarrollo de este proyecto semestral, mi aprendizaje estuvo centrado en comprender el funcionamiento interno de los modelos de lenguaje y la física detrás del almacenamiento vectorial. Entender cómo un pipeline RAG convierte documentos no estructurados en trozos de texto y los transforma a través de modelos de embeddings como <code>all-MiniLM-L6-v2</code> en vectores de números reales (arrays multidimensionales) fue revelador. Comprender que la búsqueda semántica no es una coincidencia de palabras clave, sino un cálculo matemático de similitud de coseno en un espacio vectorial de alta dimensión, me permitió asimilar cómo los modelos logran recuperar información relevante y coherente sin requerir bases de datos relacionales tradicionales.</p>

<p style="text-align: justify;">El aprendizaje más significativo de la asignatura fue la implementación del paradigma de control de flujo ReAct (Reasoning and Acting). Analizar cómo un LLM descompone un objetivo abstracto en tokens de planificación lógica interna ("Thought"), invocación estructurada de funciones ("Action") y captura de retornos de ejecución ("Observation") a través de la integración de herramientas me demostró el enorme potencial del procesamiento secuencial ordenado frente a la generación directa tradicional. Asimismo, comprender el dilema de la ventana de contexto ($k$-Window) y cómo un historial muy inflado degrada la atención interna de las neuronas del modelo (provocando alucinaciones o pérdida de instrucciones iniciales) me enseñó que la ingeniería de prompts es un balance de control de flujo e inyección de contexto riguroso.</p>

<p style="text-align: justify;">Por último, el mayor desafío técnico fue entender el funcionamiento de la autoevaluación automatizada mediante LLM-as-a-Judge. Estudiar cómo un modelo validador (Gemini) puede actuar de forma independiente aplicando rúbricas y criterios lógicos estrictos para evaluar la veracidad y precisión de otro agente inteligente me demostró que el monitoreo de soluciones cognitivas requiere de arquitecturas de evaluación paralelas. Esta experiencia consolidó mi comprensión de que diseñar sistemas inteligentes no se trata solo de consumir APIs en la nube, sino de implementar barreras de control de contexto, validación de fidelidad de respuestas y resiliencia offline para garantizar la estabilidad del sistema.</p>

---

## 7. Declaración de Uso de Asistentes de Inteligencia Artificial

<p style="text-align: justify;">De acuerdo con las políticas del uso ético de Inteligencia Artificial de Duoc UC, se declara de forma transparente el uso de asistentes de IA en las siguientes dimensiones del proyecto:</p>

<ul>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Herramienta Utilizada</strong>: Antigravity AI Coding Assistant (basado en Gemini 3.5 Flash).</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Desarrollo de Software y Aplicaciones</strong>: Se utilizó el asistente como copiloto de programación para configurar el backend en FastAPI (main.py), la integración de CORS, la definición de las rutas de servicio y los adaptadores de bases de datos. Asimismo, se utilizó para la estructuración de la aplicación frontend en React (Vite) y el diseño del panel de observabilidad en Streamlit con gráficos de Plotly.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Lógica del Agente e Infraestructura</strong>: Se contó con asistencia de IA en la programación inicial de las herramientas (tools) de LangChain, el TripleFallbackLLMProvider, los módulos de planificación en planner.py, y la estructuración del archivo de observabilidad agent_observability.jsonl.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Redacción y Diagramación</strong>: Se empleó la IA como apoyo para la corrección gramatical de la documentación, la organización del formato Markdown, la creación de diagramas de secuencia y flujo en formato Mermaid, y la inserción de enlaces de navegabilidad en el notebook de observabilidad.</li>
    <li style="text-align: justify; margin-bottom: 8px;"><strong>Originalidad y Validación</strong>: La definición conceptual del problema logístico, la elección estratégica de Clean Architecture, las decisiones de diseño ante variables de estacionalidad clima-inventario, y la posterior revisión y validación de todo el código generado fueron lideradas y ejecutadas por el equipo del proyecto, asegurando su correcto funcionamiento local.</li>
</ul>

---

## 8. Referencias (APA)

* Martin, R. C. (2012). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
* LangChain Community. (2024). *Retrieval-Augmented Generation (RAG) Conceptual Documentation*. Recuperado de https://js.langchain.com/docs/concepts/rag
* Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *arXiv preprint arXiv:1908.10084*.
