# Agente de Logística Inteligente — OmniRetail S.A.

Este proyecto implementa un **Agente Inteligente Conversacional (ALI)** diseñado para la asignatura *Ingeniería de Soluciones con Inteligencia Artificial (ISY0101) - Evaluación Parcial 2*.

---

## Inicio Rápido

### 1. Requisitos Previos
- Python 3.9+
- Una clave de API (configurada en [.env](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/.env)) como `GITHUB_TOKEN` o `GOOGLE_API_KEY`.

### 2. Instalación
Clona el repositorio e instala las dependencias indicadas en [requirements.txt](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/requirements.txt):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuración
Copia el archivo [.env.example](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/.env.example) a [.env](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/.env) y configura tus tokens:
```bash
cp .env.example .env
```
*(Asegúrate de registrar tus API keys en [.env](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/.env) para habilitar el agente Online LLM).*

### 4. Inicializar Datos
Genera la base de datos SQLite ejecutando [scripts/setup_db.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/scripts/setup_db.py) y carga los documentos de política en la base de datos vectorial ChromaDB ejecutando [scripts/ingest_docs.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/scripts/ingest_docs.py):
```bash
python scripts/setup_db.py
PYTHONPATH=. python scripts/ingest_docs.py
```

### 5. Ejecutar la Aplicación

Tenés dos opciones para ejecutar el proyecto (la opción automática es la recomendada):

#### Opción A: Ejecución Automática (Recomendada)
Ejecutá el script de arranque [start.sh](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/start.sh) en la raíz. Este script levantará el Backend y el Frontend en paralelo, registrará el kernel de Jupyter del entorno virtual y detendrá todo de forma segura cuando presiones `CTRL+C`:
```bash
./start.sh
```

#### Opción B: Ejecución Manual
Si preferís iniciar los servicios por separado en distintas terminales:

1. **Iniciar el Backend API:**
   Inicia el servidor en [backend/main.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/main.py):
   ```bash
   .venv/bin/python -m uvicorn main:app --app-dir backend --host 0.0.0.0 --port 18050 --reload
   ```

2. **Iniciar el Frontend (React + Vite):**
   Entra a la carpeta [frontend/](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/frontend) e inicia el servidor con `pnpm`:
   ```bash
   cd frontend
   pnpm run dev --host 0.0.0.0 --port 19051
   ```

*También podés explorar e interactuar de forma aislada con el notebook interactivo abriendo [notebooks/demo.ipynb](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/notebooks/demo.ipynb) ejecutando:*
```bash
jupyter notebook notebooks/demo.ipynb
```

---

## Arquitectura

El sistema sigue los principios de **Clean Architecture** (Robert C. Martin), separando claramente el dominio, casos de uso, adaptadores e infraestructura. Para más detalles conceptuales, consulta [docs/arquitectura.md](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/docs/arquitectura.md) y el resumen técnico en [LearningIA.md](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/LearningIA.md).

---

## Herramientas Autónomas Implementadas

1.  **Consultar Inventario** ([inventory_query.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/inventory_query.py)): Recupera el stock físico y en tránsito de SQLite.
2.  **Analizar Tendencias** ([trend_analyzer.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/trend_analyzer.py)): Calcula promedios de ventas históricas.
3.  **Consultar Clima** ([weather_checker.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/weather_checker.py)): Recupera pronósticos que afectan ventas estacionales.
4.  **Buscador de Políticas (RAG)** ([recommendation_engine.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/recommendation_engine.py)): Recupera reglas de negocio desde ChromaDB.
5.  **Escribir Reporte** ([report_writer.py](file:///home/hector/Escritorio/SolucionesIA/SolucionesIA/backend/src/tools/report_writer.py)): Persiste recomendaciones justificadas en disco.

---

## Autor

- Héctor Águila
