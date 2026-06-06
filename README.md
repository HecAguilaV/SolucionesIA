# Agente de Gestión de Inventario — OmniRetail S.A.

Este proyecto implementa un **Agente Inteligente Conversacional** diseñado para la asignatura *Ingeniería de Soluciones con Inteligencia Artificial (ISY0101) - Evaluación Parcial 2*.

## 🚀 Inicio Rápido

### 1. Requisitos Previos
- Python 3.9+
- Una clave de API (GitHub Models `GITHUB_TOKEN` o `GOOGLE_API_KEY`)

### 2. Instalación
Clona el repositorio e instala las dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuración
Copia el archivo `.env.example` a `.env` y configura tus tokens:
```bash
cp .env.example .env
```
*(Asegúrate de llenar `GITHUB_TOKEN` en tu archivo `.env`)*

### 4. Inicializar Datos
Genera la base de datos sintética y carga los documentos de política en la base de datos vectorial (ChromaDB):
```bash
python scripts/setup_db.py
PYTHONPATH=. python scripts/ingest_docs.py
```

### 5. Ejecutar la Aplicación
Inicia la interfaz de usuario con Streamlit:
```bash
streamlit run app.py
```
*También puedes explorar el notebook interactivo ejecutando `jupyter notebook notebooks/demo.ipynb`.*

## 🏗️ Arquitectura
El sistema sigue los principios de **Clean Architecture** (Robert C. Martin), separando claramente el dominio, casos de uso, adaptadores e infraestructura. Para más detalles, consulta `docs/arquitectura.md`.

## 🛠️ Herramientas Autónomas Implementadas
1. **Consultar Inventario**: Recupera el stock físico y en tránsito (SQL).
2. **Analizar Tendencias**: Calcula promedios de ventas históricas.
3. **Consultar Clima**: Recupera pronósticos que afectan ventas estacionales.
4. **Buscador de Políticas (RAG)**: Recupera reglas de negocio desde ChromaDB.
5. **Escribir Reporte**: Persiste recomendaciones justificadas en disco.

## 🤝 Integrantes
- Héctor Águila
- (Antigravity IA Assistant)