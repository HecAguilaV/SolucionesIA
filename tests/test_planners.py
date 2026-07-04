import pytest
from src.application.planner import (
    PlanningStrategy,
    GoalOrientedPlanner,
    HierarchicalPlanner,
    ReactivePlanner,
    Plan,
    PlanStep
)

# Mock (Proveedor LLM Falso) para simular respuestas estructuradas del planificador en los tests
class MockLLMProvider:
    def __init__(self, response: str):
        self.response = response
        
    def generate_response(self, prompt: str) -> str:
        # Devuelve el texto estructurado del plan
        return self.response

def test_goal_oriented_planner_structured():
    """
    Test 1: Verifica que el planificador orientado a objetivos parsea correctamente
    el texto devuelto por el LLM cuando cumple con el formato estructurado 'STEP:'.
    """
    mock_llm = MockLLMProvider(
        "STEP: consultar_inventario | Consultar stock físico | Stock obtenido\n"
        "STEP: buscar_politicas_empresa | Buscar reglas internas | Reglas obtenidas"
    )
    planner = GoalOrientedPlanner(mock_llm)
    plan = planner.create_plan("Quiero ver stock y aplicar políticas")
    
    # Comprobar estrategia y mapeo correcto de las acciones
    assert plan.strategy == PlanningStrategy.GOAL_ORIENTED
    assert len(plan.steps) == 2
    assert plan.steps[0].action == "consultar_inventario"
    assert plan.steps[0].expected_outcome == "Stock obtenido"
    assert plan.steps[1].action == "buscar_politicas_empresa"
    
def test_goal_oriented_planner_fallback():
    """
    Test 2: Verifica la contingencia del planificador orientado a objetivos.
    Si el LLM no responde en el formato estructurado 'STEP:', el planificador
    no se rompe y encapsula todo el texto plano en un paso único 'ejecutar_plan_llm'.
    """
    mock_llm = MockLLMProvider("Esto no tiene formato de pasos.")
    planner = GoalOrientedPlanner(mock_llm)
    plan = planner.create_plan("Hacer plan general")
    
    assert plan.strategy == PlanningStrategy.GOAL_ORIENTED
    assert len(plan.steps) == 1
    assert plan.steps[0].action == "ejecutar_plan_llm"
    assert plan.steps[0].description == "Esto no tiene formato de pasos."

def test_hierarchical_planner_sorting():
    """
    Test 3: Verifica que el planificador jerárquico ordene los pasos por prioridad.
    El planificador debe priorizar HIGH (3), luego MEDIUM (2) y por último LOW (1),
    independientemente del orden en que los devuelva el LLM.
    """
    mock_llm = MockLLMProvider(
        "STEP: LOW | consultar_inventario | Consultar stock | Stock obtenido\n"
        "STEP: HIGH | plan_general | Definir plan logístico | Plan definido\n"
        "STEP: MEDIUM | analizar_datos | Analizar coherencia de datos | Datos analizados"
    )
    planner = HierarchicalPlanner(mock_llm)
    plan = planner.create_plan("Investigar stock con estrategia")
    
    assert plan.strategy == PlanningStrategy.HIERARCHICAL
    assert len(plan.steps) == 3
    # Comprobar que el primer paso en ejecutarse sea el estratégico de prioridad HIGH (3)
    assert plan.steps[0].priority == 3
    assert "HIGH" in plan.steps[0].description
    assert plan.steps[0].action == "plan_general"
    
    # Comprobar orden descendente: 3 -> 2 -> 1
    assert plan.steps[1].priority == 2
    assert plan.steps[2].priority == 1

def test_reactive_planner_low_stock():
    """
    Test 4: Verifica que el planificador reactivo genere los pasos adecuados
    basándose en reglas de coincidencia de palabras clave para solicitudes de stock bajo.
    Este planificador es determinista y no consume tokens de LLM.
    """
    planner = ReactivePlanner(None)  # No consume LLM, el proveedor puede ser None
    plan = planner.create_plan("Quiero reponer los productos con stock bajo")
    
    assert plan.strategy == PlanningStrategy.REACTIVE
    # El plan debe detonar de forma determinista la consulta y la escritura de reporte
    assert any(step.action == "consultar_inventario" for step in plan.steps)
    assert any(step.action == "escribir_reporte" for step in plan.steps)
    
def test_reactive_planner_weather():
    """
    Test 5: Verifica que el planificador reactivo agregue la consulta del clima
    cuando la solicitud del usuario coincide con términos meteorológicos.
    """
    planner = ReactivePlanner(None)
    plan = planner.create_plan("Verificar el pronóstico del clima y cómo impacta en las ventas")
    
    assert plan.strategy == PlanningStrategy.REACTIVE
    assert any(step.action == "consultar_clima" for step in plan.steps)
