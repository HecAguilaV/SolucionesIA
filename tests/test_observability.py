import pytest
import os
import json
from src.infrastructure.observability import ObservabilityManager, OBSERVABILITY_LOG_PATH

# Proveedor de LLM Falso (Mock) para simular respuestas del evaluador en los tests
class MockLLMProvider:
    def __init__(self, response: str):
        self.response = response
        
    def generate_response(self, prompt: str) -> str:
        # Retorna el puntaje de calidad simulado (ej: "95")
        return self.response

def test_observability_logging_success(tmp_path):
    """
    Test 1: Verifica el registro exitoso de una interacción en los logs de observabilidad.
    Comprueba que los tiempos, consultas, herramientas y el score de precisión
    calculado por el LLM-as-a-Judge se almacenen correctamente en el archivo físico.
    """
    # Usar una ruta temporal provista por pytest para no alterar los logs de producción
    test_log_path = tmp_path / "test_observability.jsonl"
    
    # Parchear temporalmente la ruta del archivo de logs para redirigirla al directorio temporal
    import src.infrastructure.observability as obs
    original_path = obs.OBSERVABILITY_LOG_PATH
    obs.OBSERVABILITY_LOG_PATH = str(test_log_path)
    
    try:
        # Inicializar el manager con un LLM mockeado que devolverá un score de "95"
        mock_llm = MockLLMProvider("95")
        manager = ObservabilityManager(mock_llm)
        
        # Registrar una interacción simulada de éxito
        entry = manager.log_interaction(
            query="¿Cuál es el stock de gaseosas?",
            response="Hay 12 unidades en la bodega central.",
            latency_sec=1.234,
            status="success",
            tools_used=["consultar_inventario"]
        )
        
        # Validaciones lógicas sobre la estructura de la telemetría devuelta
        assert entry["query"] == "¿Cuál es el stock de gaseosas?"
        assert entry["latency_sec"] == 1.234
        assert entry["status"] == "success"
        assert entry["tools_used"] == ["consultar_inventario"]
        assert entry["accuracy_eval"] == 95 # Valida que la respuesta del LLM-as-a-judge fue parseada como int
        
        # Validaciones físicas: Verificar que el archivo JSONL se creó y contiene la traza
        assert os.path.exists(obs.OBSERVABILITY_LOG_PATH)
        with open(obs.OBSERVABILITY_LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 1 # Debe haber una sola línea en el archivo
            logged_entry = json.loads(lines[0])
            # Comprobar que el ID registrado coincide con el ID generado en la interacción
            assert logged_entry["query_id"] == entry["query_id"]
            
    finally:
        # Restaurar la constante original del path de logs para no romper la app
        obs.OBSERVABILITY_LOG_PATH = original_path

def test_observability_logging_error(tmp_path):
    """
    Test 2: Verifica el registro de una interacción fallida (Error).
    Comprueba que las excepciones del agente se capturen correctamente en los logs,
    guardando el mensaje del error y dejando la precisión (accuracy_eval) vacía (None).
    """
    test_log_path = tmp_path / "test_observability.jsonl"
    
    # Parchear temporalmente la ruta del archivo de logs
    import src.infrastructure.observability as obs
    original_path = obs.OBSERVABILITY_LOG_PATH
    obs.OBSERVABILITY_LOG_PATH = str(test_log_path)
    
    try:
        # Inicializar el manager sin LLM (para emular fallas de conexión o modo offline)
        manager = ObservabilityManager(None)
        
        # Registrar una interacción simulada que arrojó una excepción (timeout)
        entry = manager.log_interaction(
            query="Consulta errónea",
            response="Ocurrió un error interno",
            latency_sec=0.5,
            status="error",
            error_message="API connection timeout",
            tools_used=[]
        )
        
        # Validaciones sobre el comportamiento del log de error
        assert entry["status"] == "error"
        assert entry["error_message"] == "API connection timeout"
        assert entry["accuracy_eval"] is None # En caso de error, no debe correr evaluación de precisión
        
    finally:
        # Restaurar la constante original
        obs.OBSERVABILITY_LOG_PATH = original_path
