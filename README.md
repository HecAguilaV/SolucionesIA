# Agente de Logística Inteligente — OmniRetail S.A. (Evaluación Parcial 1)

Este directorio contiene el código y la documentación técnica desarrollados para la **Evaluación Parcial N°1 (EP1)** de la asignatura *Ingeniería de Soluciones con Inteligencia Artificial (ISY0101)*. 

Esta primera fase se centra exclusivamente en el **Diseño de la Solución de Inteligencia Artificial, Formulación de Prompts y el Pipeline de Recuperación Aumentada (RAG)** para asistir en la gestión de stock e inventario de OmniRetail S.A.

---

## Estructura del Proyecto en esta Fase

*   `src/`: Código fuente de las capas del proyecto.
    *   `src/domain/`: Interfaces y entidades del negocio.
    *   `src/infrastructure/`: Adaptadores de base de datos (SQLite), proveedor de LLM y almacenamiento vectorial.
    *   `src/memory/`: Lógica de recuperación semántica (RAG) con `SemanticRetriever`.
*   `data/`:
    *   `data/docs/`: Políticas y guías corporativas de OmniRetail (`politica_inventario.md` y `guia_reposicion.md`).
    *   `data/omniretail.db`: Base de datos SQLite inicial.
*   `docs/`:
    *   `docs/Informe_Tecnico_Ev1.md`: Informe técnico completo del diseño y arquitectura RAG.
*   `scripts/`:
    *   `scripts/setup_db.py`: Inicializa la base de datos SQLite y carga datos sintéticos.
    *   `scripts/ingest_docs.py`: Divide los documentos de políticas y los inserta indexados en la base vectorial ChromaDB.
    *   `scripts/demo_rag.py`: Script para probar consultas en lenguaje natural usando el pipeline RAG y el LLM.

---

## Instrucciones de Ejecución

### 1. Configuración de Entorno

Crea el entorno virtual e instala las dependencias del proyecto:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz (puedes guiarte por `.env.example`) y configura tu clave de API para habilitar la llamada al LLM:
```env
GOOGLE_API_KEY=tu_gemini_api_key_aqui
```

### 2. Inicializar Bases de Datos

1.  **SQLite (Estructurado)**: Crea las tablas de inventario y ventas con datos iniciales:
    ```bash
    python scripts/setup_db.py
    ```

2.  **ChromaDB (No Estructurado - RAG)**: Procesa e indexa las políticas corporativas en la base de datos vectorial local:
    ```bash
    PYTHONPATH=. python scripts/ingest_docs.py
    ```

### 3. Probar el Pipeline RAG

Ejecuta el script de demostración de RAG para realizar consultas en lenguaje natural al corpus de políticas internas:
```bash
PYTHONPATH=. python scripts/demo_rag.py --query "¿Cuál es la política para quiebres de stock?"
```

---

## Documentación
El informe técnico completo con la justificación del diseño, formulación de prompts y arquitectura se encuentra disponible en:
*   [Informe Técnico EP1 (Markdown)](docs/Informe_Tecnico_Ev1.md)
