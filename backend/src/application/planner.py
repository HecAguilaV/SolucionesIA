from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional
from src.infrastructure.llm_provider import TripleFallbackLLMProvider

class PlanningStrategy(Enum):
    HIERARCHICAL = "hierarchical"
    REACTIVE = "reactive"
    GOAL_ORIENTED = "goal_oriented"

@dataclass
class PlanStep:
    action: str
    description: str
    expected_outcome: str
    priority: int = 1
    status: str = "pending"

@dataclass
class Plan:
    goal: str
    steps: List[PlanStep]
    strategy: PlanningStrategy
    status: str = "created"

class BasePlanner(ABC):
    """
    Clase base para todos los planificadores del sistema.
    """
    def __init__(self, llm_provider: TripleFallbackLLMProvider):
        self.llm_provider = llm_provider

    @abstractmethod
    def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Plan:
        """
        Genera un plan estructurado para resolver el objetivo.
        """
        pass

class GoalOrientedPlanner(BasePlanner):
    """
    Planificador orientado a objetivos. Descompone la solicitud en pasos lógicos secuenciales.
    """
    def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Plan:
        prompt = f"""
        Eres un planificador experto en logística y gestión de inventario para OmniRetail.
        Tu objetivo es descomponer la solicitud del usuario en una secuencia lógica de pasos orientados a objetivos.
        
        Solicitud del usuario: "{goal}"
        
        Las herramientas disponibles para el agente ejecutor son:
        1. consultar_inventario: Para ver el stock físico actual.
        2. analizar_tendencias: Para ver ventas históricas.
        3. consultar_clima: Para ver el pronóstico (afecta ventas estacionales).
        4. buscar_politicas_empresa: Para leer reglas internas (RAG).
        5. escribir_reporte: Para guardar la recomendación final.
        
        Regla de negocio: SIEMPRE debes buscar políticas de la empresa ANTES de emitir un reporte final.
        
        Debes responder EXCLUSIVAMENTE con los pasos en el siguiente formato, uno por línea. No agregues introducciones, enumeraciones como "1.", ni explicaciones adicionales:
        STEP: [Nombre de la Acción] | [Descripción detallada del paso] | [Resultado esperado]
        
        Ejemplo:
        STEP: consultar_inventario | Consultar el stock actual del producto SKU123 | Stock actual obtenido
        STEP: buscar_politicas_empresa | Buscar políticas de reabastecimiento | Reglas de reabastecimiento obtenidas
        """
        
        response = self.llm_provider.generate_response(prompt)
        steps = self._parse_steps(response, goal)
        return Plan(goal=goal, steps=steps, strategy=PlanningStrategy.GOAL_ORIENTED)

    def generate_plan(self, goal: str) -> Plan:
        """
        Método de compatibilidad con la versión anterior.
        """
        return self.create_plan(goal)

    def _parse_steps(self, response: str, goal: str) -> List[PlanStep]:
        steps = []
        lines = response.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("STEP:"):
                try:
                    parts = line[5:].split("|")
                    if len(parts) >= 3:
                        action = parts[0].strip()
                        description = parts[1].strip()
                        expected_outcome = parts[2].strip()
                        steps.append(PlanStep(
                            action=action,
                            description=description,
                            expected_outcome=expected_outcome,
                            priority=1
                        ))
                except Exception:
                    pass
        
        # Fallback en caso de que falle el parseo estructurado
        if not steps:
            steps.append(PlanStep(
                action="ejecutar_plan_llm",
                description=response.strip(),
                expected_outcome="Resolución de la solicitud"
            ))
            
        return steps

class HierarchicalPlanner(BasePlanner):
    """
    Planificador jerárquico. Descompone los objetivos en niveles de abstracción (HIGH, MEDIUM, LOW).
    """
    def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Plan:
        prompt = f"""
        Eres un planificador jerárquico experto para OmniRetail. 
        Tu tarea es descomponer la solicitud del usuario en tres niveles de abstracción:
        - HIGH: Nivel estratégico/decisión (Prioridad 3)
        - MEDIUM: Nivel de análisis y validación lógica (Prioridad 2)
        - LOW: Nivel operativo de ejecución de herramientas (Prioridad 1)
        
        Solicitud del usuario: "{goal}"
        
        Las herramientas disponibles son:
        1. consultar_inventario
        2. analizar_tendencias
        3. consultar_clima
        4. buscar_politicas_empresa
        5. escribir_reporte
        
        Debes responder EXCLUSIVAMENTE con la lista de pasos en el siguiente formato, uno por línea. No agregues introducciones, comentarios ni enumeraciones:
        STEP: [HIGH/MEDIUM/LOW] | [Nombre de la Acción] | [Descripción detallada] | [Resultado esperado]
        
        Ejemplo:
        STEP: HIGH | planificacion_estrategica | Diseñar estrategia de reposición para tienda | Estrategia diseñada
        STEP: MEDIUM | analisis_logistico | Analizar stock contra políticas de la empresa | Análisis logístico completado
        STEP: LOW | consultar_inventario | Consultar stock actual en la base de datos | Stock actual obtenido
        """
        
        response = self.llm_provider.generate_response(prompt)
        steps = self._parse_steps(response, goal)
        return Plan(goal=goal, steps=steps, strategy=PlanningStrategy.HIERARCHICAL)

    def _parse_steps(self, response: str, goal: str) -> List[PlanStep]:
        steps = []
        lines = response.strip().split("\n")
        priority_map = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        
        for line in lines:
            line = line.strip()
            if line.startswith("STEP:"):
                try:
                    parts = line[5:].split("|")
                    if len(parts) >= 4:
                        level = parts[0].strip().upper()
                        action = parts[1].strip()
                        description = f"[{level}] {parts[2].strip()}"
                        expected_outcome = parts[3].strip()
                        priority = priority_map.get(level, 1)
                        
                        steps.append(PlanStep(
                            action=action,
                            description=description,
                            expected_outcome=expected_outcome,
                            priority=priority
                        ))
                except Exception:
                    pass
                    
        # Fallback en caso de fallo de parseo
        if not steps:
            steps.append(PlanStep(
                action="ejecutar_plan_jerarquico_llm",
                description=f"[HIGH] {response.strip()}",
                expected_outcome="Plan jerárquico ejecutado",
                priority=3
            ))
            
        # Ordenar por prioridad descendente (HIGH -> MEDIUM -> LOW)
        steps.sort(key=lambda x: x.priority, reverse=True)
        return steps

class ReactivePlanner(BasePlanner):
    """
    Planificador reactivo. Toma decisiones basadas en eventos y estado del entorno.
    """
    def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Plan:
        steps = []
        ctx = context or {}
        
        # Evaluar estado del entorno / palabras clave
        low_stock = ctx.get("low_stock", False) or any(w in goal.lower() for w in ["bajo", "crítico", "critico", "alerta", "reponer"])
        weather_alert = ctx.get("weather_alert", False) or any(w in goal.lower() for w in ["clima", "pronostico", "pronóstico", "lluvia", "temperatura"])
        policies_check = ctx.get("policies_check", True)
        
        if low_stock:
            steps.append(PlanStep(
                action="consultar_inventario",
                description="REACCIÓN: Stock bajo o alerta detectada. Verificar niveles de inventario físico de inmediato.",
                expected_outcome="Niveles de stock crítico obtenidos",
                priority=3
            ))
            
        if weather_alert:
            steps.append(PlanStep(
                action="consultar_clima",
                description="REACCIÓN: Contexto de clima detectado. Consultar API del clima para prever afectación en ventas estacionales.",
                expected_outcome="Información climática recuperada",
                priority=2
            ))
            
        if policies_check:
            steps.append(PlanStep(
                action="buscar_politicas_empresa",
                description="REACCIÓN: Validar restricciones y reglas internas de abastecimiento.",
                expected_outcome="Reglas de negocio y políticas obtenidas",
                priority=1
            ))
            
        # Si no se disparó ninguna regla específica, hacemos verificación general
        if not steps:
            steps.append(PlanStep(
                action="consultar_inventario",
                description="REACCIÓN: Consulta general solicitada. Verificar inventario.",
                expected_outcome="Inventario general verificado",
                priority=1
            ))
            
        # Reporte final reactivo
        if any(w in goal.lower() for w in ["reporte", "escribir", "guardar", "documentar"]) or low_stock:
            steps.append(PlanStep(
                action="escribir_reporte",
                description="REACCIÓN: Generar y documentar informe final de recomendación logística.",
                expected_outcome="Reporte guardado en archivo local",
                priority=0
            ))
            
        # Ordenar por prioridad descendente
        steps.sort(key=lambda x: x.priority, reverse=True)
        return Plan(goal=goal, steps=steps, strategy=PlanningStrategy.REACTIVE)
