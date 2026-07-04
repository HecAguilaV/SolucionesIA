import os
import json
import time
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from src.config.settings import DATA_DIR

# Ruta del archivo de logs de observabilidad
OBSERVABILITY_LOG_PATH = os.path.join(DATA_DIR, "agent_observability.jsonl")

class ObservabilityManager:
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider

    def log_interaction(self, query: str, response: str, latency_sec: float, status: str, error_message: str = None, tools_used: list = None):
        """
        Registra una interacción del agente con métricas detalladas en el archivo JSONL.
        """
        # Calcular estimación básica de tokens (aproximadamente 4 caracteres por token)
        estimated_tokens = int((len(query) + len(response)) / 4.0)
        
        # Iniciar datos básicos
        log_entry = {
            "query_id": str(uuid.uuid4()),
            "timestamp": datetime.now(ZoneInfo("America/Santiago")).isoformat(),

            "query": query,
            "response": response,
            "latency_sec": round(latency_sec, 3),
            "status": status,
            "error_message": error_message,
            "tools_used": tools_used or [],
            "tokens_estimated": estimated_tokens,
            "accuracy_eval": None
        }

        # Realizar evaluación de calidad / precisión con el LLM si está disponible y la llamada fue exitosa
        if self.llm_provider and status == "success":
            try:
                eval_prompt = f"""
                Analiza la siguiente interacción entre el usuario y el Agente de Logística Inteligente (ALI) de OmniRetail.
                
                Pregunta del usuario: "{query}"
                Respuesta del agente: "{response}"
                
                Evalúa la precisión y calidad de la respuesta en una escala del 0 al 100, considerando los siguientes criterios:
                1. Precisión de datos: ¿El agente brinda datos claros y responde directamente la consulta?
                2. Adherencia a políticas: ¿Se alinea con las reglas y políticas de inventario de la empresa (por ejemplo, puntos de reorden ROP, stock de seguridad)?
                3. Utilidad y justificación: ¿Justifica sus recomendaciones usando datos numéricos reales y coherentes?

                Responde únicamente con un número entero entre 0 y 100. No agregues explicaciones ni caracteres adicionales.
                """
                eval_res = self.llm_provider.generate_response(eval_prompt).strip()
                # Extraer solo el número por si acaso
                digits = "".join([c for c in eval_res if c.isdigit()])
                if digits:
                    log_entry["accuracy_eval"] = int(digits)
            except Exception as e:
                print(f"[WARN] Error al autoevaluar la respuesta con LLM: {e}")

        # Guardar en archivo JSONL
        try:
            with open(OBSERVABILITY_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[ERROR] No se pudo guardar el log de observabilidad: {e}")

        return log_entry
