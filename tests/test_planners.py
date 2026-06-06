import pytest
from src.application.planner import (
    PlanningStrategy,
    GoalOrientedPlanner,
    HierarchicalPlanner,
    ReactivePlanner,
    Plan,
    PlanStep
)

class MockLLMProvider:
    def __init__(self, response: str):
        self.response = response
        
    def generate_response(self, prompt: str) -> str:
        return self.response

def test_goal_oriented_planner_structured():
    mock_llm = MockLLMProvider(
        "STEP: consultar_inventario | Consultar stock físico | Stock obtenido\n"
        "STEP: buscar_politicas_empresa | Buscar reglas internas | Reglas obtenidas"
    )
    planner = GoalOrientedPlanner(mock_llm)
    plan = planner.create_plan("Quiero ver stock y aplicar políticas")
    
    assert plan.strategy == PlanningStrategy.GOAL_ORIENTED
    assert len(plan.steps) == 2
    assert plan.steps[0].action == "consultar_inventario"
    assert plan.steps[0].expected_outcome == "Stock obtenido"
    assert plan.steps[1].action == "buscar_politicas_empresa"
    
def test_goal_oriented_planner_fallback():
    mock_llm = MockLLMProvider("Esto no tiene formato de pasos.")
    planner = GoalOrientedPlanner(mock_llm)
    plan = planner.create_plan("Hacer plan general")
    
    assert plan.strategy == PlanningStrategy.GOAL_ORIENTED
    assert len(plan.steps) == 1
    assert plan.steps[0].action == "ejecutar_plan_llm"
    assert plan.steps[0].description == "Esto no tiene formato de pasos."

def test_hierarchical_planner_sorting():
    mock_llm = MockLLMProvider(
        "STEP: LOW | consultar_inventario | Consultar stock | Stock obtenido\n"
        "STEP: HIGH | plan_general | Definir plan logístico | Plan definido\n"
        "STEP: MEDIUM | analizar_datos | Analizar coherencia de datos | Datos analizados"
    )
    planner = HierarchicalPlanner(mock_llm)
    plan = planner.create_plan("Investigar stock con estrategia")
    
    assert plan.strategy == PlanningStrategy.HIERARCHICAL
    assert len(plan.steps) == 3
    # Debe estar ordenado por prioridad descendente (HIGH=3 -> MEDIUM=2 -> LOW=1)
    assert plan.steps[0].priority == 3
    assert "HIGH" in plan.steps[0].description
    assert plan.steps[0].action == "plan_general"
    
    assert plan.steps[1].priority == 2
    assert plan.steps[2].priority == 1

def test_reactive_planner_low_stock():
    planner = ReactivePlanner(None)  # ReactivePlanner no usa LLM en esta implementación, puede ser None
    plan = planner.create_plan("Quiero reponer los productos con stock bajo")
    
    assert plan.strategy == PlanningStrategy.REACTIVE
    assert any(step.action == "consultar_inventario" for step in plan.steps)
    assert any(step.action == "escribir_reporte" for step in plan.steps)
    
def test_reactive_planner_weather():
    planner = ReactivePlanner(None)
    plan = planner.create_plan("Verificar el pronóstico del clima y cómo impacta en las ventas")
    
    assert plan.strategy == PlanningStrategy.REACTIVE
    assert any(step.action == "consultar_clima" for step in plan.steps)
