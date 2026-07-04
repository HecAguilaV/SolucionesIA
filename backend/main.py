from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import sys

# Asegurar que 'backend' esté en el path de búsqueda de módulos para resolver imports de 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.application.agent import InventoryAgent
from src.config.settings import DB_PATH, CHROMA_PERSIST_DIR

app = FastAPI(title="OmniRetail Inventory Agent API")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar el agente inteligente
try:
    agent = InventoryAgent()
except Exception as e:
    print(f"[ERROR] No se pudo inicializar el agente: {e}")
    agent = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.on_event("startup")
def startup_event():
    print("Verificando accesibilidad de bases de datos...")
    if not os.path.exists(DB_PATH):
        print(f"[WARNING] SQLite DB no encontrada en {DB_PATH}. Corra 'python scripts/setup_db.py' primero.")
    else:
        print(f"[OK] SQLite DB encontrada en {DB_PATH}.")
        
    if not os.path.exists(CHROMA_PERSIST_DIR):
        print(f"[WARNING] ChromaDB no encontrado en {CHROMA_PERSIST_DIR}. Corra 'python scripts/ingest_docs.py' primero.")
    else:
        print(f"[OK] ChromaDB encontrado en {CHROMA_PERSIST_DIR}.")

@app.get("/api/health")
def health_check():
    active_warehouses = 0
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT ubicacion) FROM inventory")
            active_warehouses = cursor.fetchone()[0]
            conn.close()
        except Exception as e:
            print(f"[ERROR] No se pudo contar las bodegas: {e}")
            active_warehouses = 3  # Fallback
            
    return {
        "status": "ok",
        "database": "connected" if os.path.exists(DB_PATH) else "missing",
        "chromadb": "connected" if os.path.exists(CHROMA_PERSIST_DIR) else "missing",
        "agent_llm": "online" if (agent and agent.agent_llm is not None) else "offline",
        "active_warehouses": active_warehouses
    }

@app.get("/api/inventory/critical")
def get_critical_inventory():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database file not found")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = """
        SELECT p.name, i.sku, i.stock_actual, i.stock_transito, i.ubicacion 
        FROM inventory i 
        JOIN products p ON i.sku = p.sku 
        WHERE i.stock_actual <= 10
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                "product": row[0],
                "sku": row[1],
                "stock": row[2],
                "transit": row[3],
                "location": row[4]
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/agent/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    if not agent:
        raise HTTPException(status_code=500, detail="Inventory Agent not initialized")
    try:
        response = agent.process_request(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

from src.infrastructure.observability import OBSERVABILITY_LOG_PATH
import json

@app.get("/api/metrics")
def get_observability_metrics():
    if not os.path.exists(OBSERVABILITY_LOG_PATH):
        return []
    try:
        metrics = []
        with open(OBSERVABILITY_LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    metrics.append(json.loads(line))
        return metrics[::-1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading metrics: {str(e)}")


