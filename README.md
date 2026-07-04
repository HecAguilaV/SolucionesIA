# Agente de Logística Inteligente — OmniRetail S.A.

Este proyecto implementa un **Agente Inteligente Conversacional (ALI)** y su respectiva **Suite de Observabilidad y Monitoreo**, desarrollado para la asignatura *Ingeniería de Soluciones con Inteligencia Artificial (ISY0101) - Evaluación Parcial 3*.

---

## Inicio Rápido

### 1. Requisitos Previos
- Python 3.9+
- Node.js & pnpm (para el frontend de React)
- Una clave de API configurada en `.env` como `GITHUB_TOKEN` o `GOOGLE_API_KEY`.

### 2. Instalación
Clona el repositorio e instala las dependencias del backend:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

E instala las dependencias del frontend:
```bash
cd frontend
CI=true pnpm install
cd ..
```

### 3. Configuración
Copia el archivo `.env.example` a `.env` y configura tus tokens:
```bash
cp .env.example .env
```
*(Asegúrate de registrar tus API keys para habilitar el agente Online LLM en la nube).*

### 4. Inicializar Datos y Telemetría
Genera la base de datos SQLite y carga los documentos de política en la base de datos vectorial ChromaDB:
```bash
python scripts/setup_db.py
PYTHONPATH=backend python scripts/ingest_docs.py
```

**Poblar Telemetría de Prueba:**
Para evaluar el dashboard con datos históricos simulados, ejecuta:
```bash
.venv/bin/python scripts/populate_telemetry.py
```

### 5. Ejecutar la Aplicación

#### Opción A: Ejecución Automática (Recomendada)
Ejecuta el script de arranque `start.sh` en la raíz. Este script levantará el Backend API, el Frontend React y el Dashboard de Streamlit en paralelo:
```bash
./start.sh
```

**Direcciones de acceso:**
*   **Frontend Chat (React):** http://localhost:19051
*   **Dashboard de Observabilidad (Streamlit):** http://localhost:18052
*   **Backend API (Swagger Docs):** http://localhost:18050/docs

#### Opción B: Ejecución Manual
Si prefieres iniciar los servicios por separado:

1.  **Iniciar Backend (FastAPI):**
    ```bash
    .venv/bin/python -m uvicorn main:app --app-dir backend --host 0.0.0.0 --port 18050 --reload
    ```
2.  **Iniciar Dashboard (Streamlit):**
    ```bash
    .venv/bin/streamlit run backend/dashboard.py --server.port 18052 --server.headless true
    ```
3.  **Iniciar Frontend (React):**
    ```bash
    cd frontend
    pnpm run dev --host 0.0.0.0 --port 19051
    ```

#### Opción C: Notebook Interactivo de Demostración (Defensa)
Para una inspección paso a paso de la ejecución del agente, llamadas a herramientas, generación de telemetría y gráficos Plotly en vivo (ideal para la defensa oral), puedes ejecutar:
```bash
.venv/bin/jupyter notebook notebooks/demo_observabilidad.ipynb
```

---


## Pruebas Automatizadas

Para validar el funcionamiento del sistema de observabilidad y trazabilidad, ejecuta:
```bash
PYTHONPATH=backend .venv/bin/python -m pytest tests/test_observability.py
```

---

## Arquitectura de Observabilidad y Métricas (Evaluación 3)

El sistema de observabilidad implementa y registra cuatro métricas clave para auditoría:
1.  **Latencia de Respuesta:** Tiempo exacto de cómputo del agente.
2.  **Frecuencia de Errores:** Registro de fallas capturadas y desvíos automáticos a contingencia.
3.  **Uso de Recursos:** Herramientas de LangChain utilizadas y tokens consumidos.
4.  **Precisión (LLM-as-a-Judge):** Autoevaluación de la respuesta basada en hechos e inventario real.

Toda la telemetría se guarda en formato JSON Lines estructurado en `data/agent_observability.jsonl` y se consume en vivo desde el Dashboard de Streamlit.

---

## Seguridad y Uso Responsable
*   **Modo Offline Fallback:** Si las APIs de LLM caen, el agente entra en modo seguro local, resolviendo consultas de stock directamente mediante consultas SQL puras sobre la base SQLite local, garantizando disponibilidad y privacidad de los datos.

---

## Autor
- Héctor Águila
