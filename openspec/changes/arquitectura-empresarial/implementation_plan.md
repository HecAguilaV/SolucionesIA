# Upgrade a Arquitectura Empresarial (FastAPI + React/Vite)

La aplicación actual en Streamlit sirvió como una Prueba de Concepto (PoC) rápida para validar la lógica del agente, la base de datos y el RAG. Sin embargo, para responder a las necesidades reales de **OmniRetail S.A.** (más de 10,000 SKUs, integración con ERPs como SAP, y la necesidad de una interfaz rica y explicativa para los jefes de tienda), necesitamos una arquitectura verdaderamente profesional.

## Objetivo
Migrar de un monolito simple (Streamlit) a un sistema desacoplado moderno (Backend API + Frontend React), enfocado en la **explicabilidad** y una **UX Premium** para la toma de decisiones logísticas.

## Propuesta de Cambios

### 1. Backend: API RESTful (FastAPI)
Para integrarse conceptualmente con un ERP (SAP/Dynamics), el agente no puede vivir dentro de la UI. Debe ser un servicio independiente y consumible vía API.
- **`backend/main.py`**: Punto de entrada de FastAPI.
- **Rutas API**:
  - `GET /api/inventory/critical`: Retorna KPIs y métricas de stock.
  - `POST /api/agent/chat`: Endpoint donde el frontend envía las consultas del usuario y el Agente de LangChain retorna la respuesta estructurada y justificada.

### 2. Frontend: Dashboard Moderno (React + Vite)
Reemplazaremos Streamlit por una aplicación web moderna (A2UI - Agent to UI).
- **Dashboard Global**: Vista de alto nivel con KPIs (Quiebres de stock proyectados, Sobrestock, Alertas climáticas).
- **Chat/Copiloto de Inventario**: Interfaz principal del usuario donde el agente no solo responde con texto plano, sino que la interfaz es capaz de renderizar componentes visuales (tablas, gráficos) si el agente los envía.
- **Diseño "WOW"**: Uso de CSS moderno, tipografía limpia (Inter/Roboto), diseño limpio corporativo, soporte para modo oscuro y animaciones dinámicas que brinden una experiencia de usuario (UX) corporativa pero vanguardista.

## Tareas a Ejecutar

#### [NUEVO] `backend/`
- Mover toda la lógica de `src/` al directorio `backend/`.
- Crear `backend/main.py` (App de FastAPI).
- Modificar `AgentExecutor` para que funcione asíncronamente y retorne datos estructurados.

#### [NUEVO] `frontend/`
- Inicializar app React/Vite (`npx create-vite-app`).
- Implementar el sistema de diseño (CSS puro para máximo control).
- Crear componentes: `Sidebar`, `KPICards`, `AgentChat`.
- Conectar con el backend.

#### [ELIMINAR]
- `app.py` (Se elimina Streamlit).

> [!IMPORTANT]
> **Revisión del Usuario Requerida**
> 
> Esta es una reestructuración profunda que convertirá el proyecto en un producto final "Enterprise-ready" mucho más robusto. Tomará algo más de tiempo ejecutarla.

## Preguntas Abiertas
1. **Estilos**: Por las directrices de diseño, suelo usar Vanilla CSS para un control total de la estética "Premium", pero si prefieres **TailwindCSS** (muy común en empresas), confírmame qué versión usar (ej: v3 o v4).
2. **Framework Frontend**: ¿Te parece bien usar React + Vite para máxima velocidad y una SPA limpia?
