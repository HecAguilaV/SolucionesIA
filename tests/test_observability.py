import pytest
import os
import json
from src.infrastructure.observability import ObservabilityManager, OBSERVABILITY_LOG_PATH

class MockLLMProvider:
    def __init__(self, response: str):
        self.response = response
        
    def generate_response(self, prompt: str) -> str:
        return self.response

def test_observability_logging_success(tmp_path):
    # Usar una ruta temporal para no alterar los logs de producción en los tests
    test_log_path = tmp_path / "test_observability.jsonl"
    
    # Parchear temporalmente la constante del módulo
    import src.infrastructure.observability as obs
    original_path = obs.OBSERVABILITY_LOG_PATH
    obs.OBSERVABILITY_LOG_PATH = str(test_log_path)
    
    try:
        mock_llm = MockLLMProvider("95")
        manager = ObservabilityManager(mock_llm)
        
        entry = manager.log_interaction(
            query="¿Cuál es el stock de gaseosas?",
            response="Hay 12 unidades en la bodega central.",
            latency_sec=1.234,
            status="success",
            tools_used=["consultar_inventario"]
        )
        
        assert entry["query"] == "¿Cuál es el stock de gaseosas?"
        assert entry["latency_sec"] == 1.234
        assert entry["status"] == "success"
        assert entry["tools_used"] == ["consultar_inventario"]
        assert entry["accuracy_eval"] == 95
        
        # Verificar archivo físico
        assert os.path.exists(obs.OBSERVABILITY_LOG_PATH)
        with open(obs.OBSERVABILITY_LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 1
            logged_entry = json.loads(lines[0])
            assert logged_entry["query_id"] == entry["query_id"]
            
    finally:
        obs.OBSERVABILITY_LOG_PATH = original_path

def test_observability_logging_error(tmp_path):
    test_log_path = tmp_path / "test_observability.jsonl"
    
    import src.infrastructure.observability as obs
    original_path = obs.OBSERVABILITY_LOG_PATH
    obs.OBSERVABILITY_LOG_PATH = str(test_log_path)
    
    try:
        manager = ObservabilityManager(None)
        
        entry = manager.log_interaction(
            query="Consulta errónea",
            response="Ocurrió un error interno",
            latency_sec=0.5,
            status="error",
            error_message="API connection timeout",
            tools_used=[]
        )
        
        assert entry["status"] == "error"
        assert entry["error_message"] == "API connection timeout"
        assert entry["accuracy_eval"] is None
        
    finally:
        obs.OBSERVABILITY_LOG_PATH = original_path
