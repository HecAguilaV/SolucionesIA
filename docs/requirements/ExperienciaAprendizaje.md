## EA 2 - Desarrollo de Agentes Inteligentes con LLM

**Resultado de Aprendizaje:** RA2

**Descripción:**
En la segunda experiencia de aprendizaje, los estudiantes desarrollan competencias avanzadas en la construcción de agentes inteligentes basados en LLM.

Se enfatiza la comprensión del paradigma de agentes autónomos, la integración de herramientas externas, el manejo de memoria y las estrategias de planificación. A lo largo de la experiencia, se analizan arquitecturas de agentes LLM, diferenciando componentes como herramientas, memoria, planificación y ejecución.

Se trabaja con frameworks especializados para agentes, explorando function calling, integración con APIs y bases de datos, y protocolos como MCP. El enfoque práctico permite que los estudiantes construyan agentes funcionales que resuelvan tareas cognitivas complejas, fortaleciendo su capacidad para diseñar flujos de trabajo automatizados y documentar arquitecturas de sistemas inteligentes.

### Act 2.1 - Arquitectura y Frameworks de Agentes

**Indicadores de Logro:** IL2.1
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)
**N° Estudiantes:** 30
**Horas Docencia Directa:** 8 hrs
**Horas Trabajo Autónomo:** 2 hrs

**Descripción Dirigida al Docente:**
El propósito de esta actividad es comprender la arquitectura fundamental de agentes LLM y dominar frameworks especializados para construir agentes funcionales que integren herramientas de consulta, escritura y razonamiento.

**Primera sesión (2 horas):** La/el docente introduce el paradigma de agentes inteligentes explicando conceptos de autonomía, razonamiento y arquitectura básica (herramientas, memoria, planificación, ejecución), comparando diferentes enfoques arquitectónicos y presentando frameworks especializados como LangChain y CrewAI. Las/los estudiantes configuran su entorno de desarrollo, instalan frameworks de agentes, exploran documentación técnica, implementan su primer agente básico con capacidades de consulta simple, practican function calling básico con herramientas externas simuladas y documentan la arquitectura implementada reflexionando sobre capacidades y limitaciones observadas.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de integración de herramientas, explicando patrones de diseño para agentes multi-herramienta, estrategias de orquestación de tareas y metodologías para manejo de errores en cadenas de herramientas. Las/los estudiantes desarrollan agentes que integran múltiples herramientas de consulta (APIs, bases de datos, servicios web), implementan capacidades de escritura automatizada (generación de reportes, emails, documentos), configuran herramientas de razonamiento lógico y análisis, y prueban la interoperabilidad entre diferentes tipos de herramientas en flujos de trabajo simulados.

**Tercera sesión (2 horas):** La/el docente presenta metodologías para diseño de agentes en contextos organizacionales específicos, incluyendo análisis de requerimientos, patrones de automatización empresarial y estrategias de validación de resultados en entornos simulados. Las/los estudiantes diseñan e implementan agentes especializados para casos organizacionales específicos (atención al cliente, análisis de datos, gestión de contenido), integran herramientas de consulta, escritura y razonamiento en flujos coherentes, validan el funcionamiento en escenarios simulados de automatización organizacional, y documentan el diseño completo incluyendo justificación de decisiones arquitectónicas y evaluación de capacidades del agente construido.

**Cuarta sesión (2 horas):** La/el docente facilita sesiones de presentación y evaluación cruzada donde los estudiantes demuestran sus agentes funcionales, explicando arquitectura, capacidades integradas y aplicabilidad organizacional. Las/los estudiantes presentan sus agentes desarrollados demostrando capacidades de consulta, escritura y razonamiento integradas, reciben retroalimentación de pares sobre funcionalidad y diseño, realizan pruebas cruzadas de agentes desarrollados por otros equipos, refinan sus implementaciones basándose en observaciones y feedback recibido, y consolidan documentación final incluyendo lecciones aprendidas y recomendaciones para mejoras futuras.

**Actividades Trabajo Autónomo:**

- Instalación y configuración de frameworks de agentes
- Exploración de documentación técnica de LangChain y CrewAI
- Práctica con ejemplos básicos de function calling

**Recursos de Aprendizaje:**

- 2.1.1 PPT Arquitectura de Agentes
- 2.1.2 Guía de Frameworks
- 2.1.3 Tutorial de Configuración
- Ejemplos de Código Base

**Tecnología Educativa:** Python, LLM Frameworks, APIs

**Bibliografía Obligatoria:** Introduction to Large Language Models with GPT & LangChain

### Act 2.2 - Memoria y Herramientas Externas

**Indicadores de Logro:** IL2.1, IL2.2
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)
**N° Estudiantes:** 30
**Horas Docencia Directa:** 6 hrs
**Horas Trabajo Autónomo:** 2 hrs

**Descripción Dirigida al Docente:**
El propósito de esta actividad es implementar sistemas de memoria y integrar herramientas externas en agentes, configurando procesos de memoria y recuperación de contexto para asegurar la continuidad de tareas en flujos prolongados.

**Primera sesión (2 horas):** La/el docente explica tipos de memoria (short-term y long-term), su importancia en la continuidad de tareas, técnicas de recuperación de contexto, estrategias de persistencia y presenta protocolos de integración como MCP para herramientas externas. Las/los estudiantes configuran sistemas básicos de memoria para sus agentes implementando almacenamiento de conversaciones, desarrollan mecanismos de recuperación de contexto histórico, integran herramientas externas simples usando APIs REST, prueban la persistencia de información entre sesiones y evalúan la efectividad de la memoria implementada documentando las configuraciones realizadas.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de gestión de memoria incluyendo estrategias de compresión de contexto, políticas de retención y eliminación de información, y metodologías para optimización de recuperación en flujos prolongados con múltiples tareas concurrentes. Las/los estudiantes implementan sistemas de memoria jerárquica con diferentes niveles de persistencia, desarrollan algoritmos de recuperación selectiva de contexto relevante, configuran políticas automáticas de gestión de memoria (limpieza, archivado, priorización), integran múltiples herramientas externas con gestión coordinada de contexto, y validan la continuidad efectiva en flujos de trabajo complejos y prolongados.

**Tercera sesión (2 horas):** La/el docente presenta metodologías para integración avanzada de herramientas externas usando protocolos MCP y A2A, incluyendo manejo de errores, recuperación de fallos, y estrategias de sincronización entre agentes y sistemas externos en contextos organizacionales. Las/los estudiantes implementan integraciones robustas con bases de datos empresariales, servicios web y APIs especializadas, desarrollan sistemas de recuperación automática ante fallos de herramientas externas, configuran sincronización de contexto entre múltiples agentes colaborativos, prueban la continuidad de tareas en escenarios de alta complejidad con múltiples dependencias, y documentan arquitecturas de integración con análisis de rendimiento y confiabilidad.

**Cuarta sesión (2 horas):** La/el docente facilita evaluación integral de sistemas de memoria y herramientas implementados, presentando metodologías de testing para continuidad de tareas y criterios de evaluación de efectividad en flujos prolongados. Las/los estudiantes realizan pruebas exhaustivas de continuidad en flujos de trabajo prolongados y complejos, evalúan la efectividad de recuperación de contexto en diferentes escenarios de uso, optimizan configuraciones de memoria basándose en métricas de rendimiento observadas, presentan sus implementaciones demostrando capacidades de continuidad y recuperación, y consolidan documentación técnica incluyendo recomendaciones para configuración óptima de memoria y herramientas en contextos organizacionales específicos.

**Actividades Trabajo Autónomo:**

- Investigación de técnicas de persistencia de memoria
- Exploración de APIs y servicios externos para integración
- Práctica con protocolos MCP y A2A

**Recursos de Aprendizaje:**

- 2.2.1 PPT Sistemas de Memoria
- 2.2.2 Guía de Integración MCP
- 2.2.3 Tutorial de APIs
- Plantillas de Configuración

**Tecnología Educativa:** Python, Bases de Datos, APIs REST, MCP Protocol

**Bibliografía Obligatoria:**

- Introduction to Large Language Models with GPT & LangChain
- A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)

### Act 2.3 - Planificación y Orquestación

**Indicadores de Logro:** IL2.3, IL2.4
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)
**N° Estudiantes:** 30
**Horas Docencia Directa:** 6 hrs
**Horas Trabajo Autónomo:** 2 hrs

**Descripción Dirigida al Docente:**
El propósito de esta actividad es implementar estrategias de planificación y toma de decisiones dentro de agentes, ajustando el comportamiento del sistema ante tareas con múltiples etapas y condiciones cambiantes, y documentar la orquestación de componentes.

**Primera sesión (2 horas):** La/el docente presenta estrategias fundamentales de planificación en agentes incluyendo algoritmos de toma de decisiones, técnicas para manejo de tareas multi-etapa, metodologías de adaptación ante condiciones cambiantes y principios básicos de orquestación de componentes. Las/los estudiantes implementan algoritmos básicos de planificación en sus agentes configurando árboles de decisión simples, desarrollan flujos de trabajo secuenciales con múltiples etapas definidas, programan mecanismos básicos de detección de cambios en condiciones del entorno, prueban la capacidad de adaptación del agente ante escenarios variables predefinidos, y crean diagramas iniciales de arquitectura documentando la estructura básica de componentes y sus interacciones.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de planificación incluyendo algoritmos de planificación dinámica, estrategias de re-planificación automática, manejo de dependencias complejas entre tareas, y metodologías de orquestación distribuida para sistemas multi-agente. Las/los estudiantes implementan algoritmos de planificación adaptativa que modifican estrategias en tiempo real, desarrollan sistemas de priorización dinámica de tareas basados en condiciones cambiantes, configuran mecanismos de coordinación entre múltiples componentes del agente, integran sistemas de monitoreo continuo para detección automática de cambios contextuales, prueban la robustez del sistema ante interrupciones y cambios inesperados en flujos de trabajo, y refinan diagramas de arquitectura incluyendo flujos de decisión complejos y puntos de adaptación.

**Tercera sesión (2 horas):** La/el docente presenta metodologías para documentación integral de sistemas de planificación y orquestación, incluyendo técnicas de modelado de comportamiento, estrategias de validación de decisiones, y estándares para documentación técnica de arquitecturas adaptativas en contextos organizacionales. Las/los estudiantes validan exhaustivamente el comportamiento de sus agentes en escenarios complejos con múltiples variables y condiciones cambiantes, optimizan algoritmos de planificación basándose en métricas de rendimiento y efectividad observadas, desarrollan documentación técnica completa incluyendo diagramas UML de comportamiento, especificaciones de algoritmos de decisión, y matrices de respuesta ante diferentes condiciones, presentan sus implementaciones demostrando capacidades de planificación adaptativa y toma de decisiones robusta, y consolidan documentación final con análisis de casos de uso, limitaciones identificadas y recomendaciones para implementación en entornos organizacionales reales.

**Actividades Trabajo Autónomo:**

- Estudio de algoritmos de planificación en IA
- Investigación de técnicas de orquestación de sistemas
- Práctica con herramientas de diagramación de arquitecturas

**Recursos de Aprendizaje:**

- 2.3.1 PPT Planificación de Agentes
- 2.3.2 Guía de Orquestación
- 2.3.3 Plantillas de Documentación
- Herramientas de Diagramación

**Tecnología Educativa:** Python, Herramientas de Modelado, Diagramas UML

**Bibliografía Obligatoria:**

- Introduction to Large Language Models with GPT & LangChain
- A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)

### Evaluaciones EA 2

#### Ev For 2 - Quiz Agentes de IA

**Indicadores de Logro:** IL2.1, IL2.2
**Horas Docencia Directa:** 2 hrs
**Horas Trabajo Autónomo:** 1 hrs

Quiz obligatorio de 8 preguntas sobre conceptos fundamentales de agentes de IA. Las preguntas evalúan conocimientos teóricos sobre arquitectura de agentes LLM, frameworks, tipos de memoria, function calling, integración con herramientas externas y estrategias de planificación.

**Actividades Trabajo Autónomo:**

- Estudio de material teórico sobre paradigmas de agentes
- Revisión de documentación sobre frameworks
- Investigación de conceptos sobre function calling

#### Ev For 2 - Construcción de Agente Básico

**Indicadores de Logro:** IL2.1, IL2.2, IL2.3, IL2.4
**Horas Docencia Directa:** 2 hrs (24 hrs)
**Horas Trabajo Autónomo:** 2 hrs

Los estudiantes construyen un agente básico que integre herramientas y memoria para resolver una tarea específica. Se evalúa la construcción de agentes funcionales con herramientas integradas y la configuración correcta de procesos de memoria para continuidad de tareas.

**Actividades Trabajo Autónomo:**

- Estudio de documentación técnica sobre implementación de agentes
- Recopilación de ejemplos de código
