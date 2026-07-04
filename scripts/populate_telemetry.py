import os
import json
import uuid
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Ruta del archivo de logs
LOG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../data/agent_observability.jsonl"
)

# Garantizar que el directorio data existe
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

queries = [
    ("¿Cuál es el stock actual del SKU 1001?", "El stock actual del producto es de 8 unidades en la bodega central. Se encuentra por debajo del Punto de Reorden (ROP).", 1.15, "success", ["consultar_inventario"], 95),
    ("¿Cómo impactará la lluvia de mañana en el stock?", "Se pronostica lluvia moderada en Santiago. Históricamente, las lluvias disminuyen la afluencia de público en un 15%, por lo que la demanda de helados (SKU 1002) bajará momentáneamente.", 2.45, "success", ["consultar_clima", "analizar_tendencias"], 92),
    ("Generá un reporte de reabastecimiento para el jefe de tienda.", "He generado el reporte de reabastecimiento en la ruta especificada. Se sugiere pedir 50 unidades de SKU 1001 para cubrir el stock de seguridad.", 3.82, "success", ["buscar_politicas_empresa", "escribir_reporte"], 98),
    ("¿Qué productos tienen stock crítico?", "Se detectaron 3 productos con stock menor o igual a 10 unidades (SKU 1001, SKU 1003). Se recomienda abastecer pronto.", 1.34, "success", ["consultar_inventario"], 94),
    ("¿Cuál es el ROP de la empresa para leches?", "Las políticas internas establecen un ROP basado en la venta promedio de los últimos 30 días multiplicada por el lead time más el stock de seguridad.", 1.98, "success", ["buscar_politicas_empresa"], 88),
    ("Consulta inválida provocando excepción", "Ocurrió un error al consultar el motor de recomendaciones corporativo.", 0.72, "error", ["buscar_politicas_empresa"], None),
    ("¿Cuánto vendimos la semana pasada?", "El análisis de tendencias muestra un volumen de ventas de 1,240 unidades en la categoría lácteos, representando un incremento del 5% respecto a la semana previa.", 2.11, "success", ["analizar_tendencias"], 90),
]

def generate_mock_data():
    # Eliminar archivo si existiera para empezar limpio
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)
        
    start_time = datetime.now(ZoneInfo("America/Santiago")) - timedelta(days=5)

    
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        # Generar unas 35 interacciones realistas distribuidas en los últimos 5 días
        for i in range(35):
            query_base = random.choice(queries)
            # Modificar timestamp
            timestamp = start_time + timedelta(hours=i * 3 + random.randint(0, 90))
            
            log_entry = {
                "query_id": str(uuid.uuid4()),
                "timestamp": timestamp.isoformat(),
                "query": query_base[0],
                "response": query_base[1],
                "latency_sec": round(query_base[2] + random.uniform(-0.3, 0.4), 3),
                "status": query_base[3] if random.random() > 0.08 else "error",  # 8% error rate
                "error_message": "Timeout de conexión con la API de LLM" if query_base[3] == "error" else None,
                "tools_used": query_base[4],
                "tokens_estimated": random.randint(180, 450),
                "accuracy_eval": random.randint(85, 100) if query_base[5] else None
            }
            # Ajustar error message si sale error aleatorio
            if log_entry["status"] == "error":
                log_entry["error_message"] = "Error de comunicación o timeout del modelo."
                log_entry["accuracy_eval"] = None
                log_entry["tools_used"] = []
                
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"Historial de trazabilidad simulado exitosamente en: {LOG_FILE_PATH}")

if __name__ == "__main__":
    generate_mock_data()
