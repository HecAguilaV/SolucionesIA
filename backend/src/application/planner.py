from dataclasses import dataclass
from typing import List, Optional
from src.infrastructure.llm_provider import TripleFallbackLLMProvider

@dataclass
class PlanStep:
    action: str
    description: str
    expected_outcome: str

@dataclass
class Plan:
    goal: str
    steps: List[PlanStep]

class GoalOrientedPlanner:
    def __init__(self, llm_provider: TripleFallbackLLMProvider):
        self.llm_provider = llm_provider

    def generate_plan(self, goal: str) -> Plan:
        """
        Genera un plan estructurado para resolver el objetivo de inventario del usuario.
        """
        prompt = f"""
        Eres un planificador experto en logística y gestión de inventario para OmniRetail.
        Tu objetivo es descomponer la siguiente solicitud del usuario en una secuencia lógica de pasos.
        
        Solicitud del usuario: "{goal}"
        
        Las herramientas disponibles para el agente ejecutor son:
        1. consultar_inventario: Para ver el stock físico actual.
        2. analizar_tendencias: Para ver ventas históricas.
        3. consultar_clima: Para ver el pronóstico (afecta ventas estacionales).
        4. buscar_politicas_empresa: Para leer reglas internas (RAG).
        5. escribir_reporte: Para guardar la recomendación final.
        
        Regla de negocio: SIEMPRE debes buscar políticas de la empresa ANTES de emitir un reporte final.
        
        Genera el plan en formato de lista paso a paso.
        """
        
        response = self.llm_provider.generate_response(prompt)
        
        # Parseo simple de la respuesta del LLM a un objeto Plan (en un escenario real usaríamos Pydantic OutputParser)
        # Por simplicidad, guardamos la respuesta del LLM como un único gran paso si no logramos parsearlo.
        steps = [PlanStep(action="Ejecutar Plan del LLM", description=response, expected_outcome="Resolución de la solicitud")]
        
        return Plan(goal=goal, steps=steps)
