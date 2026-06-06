from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.infrastructure.llm_provider import TripleFallbackLLMProvider
from src.memory.conversation_memory import MemoryManager
from src.application.planner import GoalOrientedPlanner
from src.tools.inventory_query import consultar_inventario
from src.tools.trend_analyzer import analizar_tendencias
from src.tools.weather_checker import consultar_clima
from src.tools.recommendation_engine import buscar_politicas_empresa
from src.tools.report_writer import escribir_reporte
from src.config.settings import AGENT_VERBOSE

class InventoryAgent:
    def __init__(self):
        # 1. Infraestructura
        self.llm_provider = TripleFallbackLLMProvider()
        self.memory_manager = MemoryManager()
        self.planner = GoalOrientedPlanner(self.llm_provider)
        
        # 2. Herramientas
        self.tools = [
            consultar_inventario,
            analizar_tendencias,
            consultar_clima,
            buscar_politicas_empresa,
            escribir_reporte
        ]
        
        # 3. LLM Nativo para LangChain Agent
        try:
            self.agent_llm = self.llm_provider.get_langchain_model()
        except ValueError:
            self.agent_llm = None
            
        # 4. Memoria
        self.memory = self.memory_manager.get_window_memory(memory_key="chat_history")
        
        # 5. Inicializar Agente
        self.executor = self._initialize_agent()

    def _initialize_agent(self):
        if not self.agent_llm:
            return None
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres ALI (Agente de Logística Inteligente) de OmniRetail.
            Tu misión es ayudar a los jefes de tienda a tomar decisiones informadas sobre logística y reposición de productos.
            
            Usa las herramientas a tu disposición para:
            1. Ver el stock y ventas (consultar_inventario, analizar_tendencias)
            2. Revisar el contexto (consultar_clima)
            3. Alinearte con las reglas de la empresa (buscar_politicas_empresa)
            4. Generar reportes finales si el usuario lo pide (escribir_reporte)
            
            Justifica siempre tus recomendaciones basándote en los datos recuperados."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(self.agent_llm, self.tools, prompt)
        
        return AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=self.memory,
            verbose=AGENT_VERBOSE,
            handle_parsing_errors=True
        )

    def process_request(self, user_input: str) -> str:
        # 1. Fallback Offline (Si no hay LLM configurado)
        if not self.executor:
            print("[WARN] Ejecutando en modo Offline Fallback (No hay API keys).")
            return self.llm_provider.generate_response(user_input)
            
        # 2. Planificación (Opcional, demuestra el concepto de IL2.3)
        if "planifica" in user_input.lower() or "estrategia" in user_input.lower():
            plan = self.planner.generate_plan(user_input)
            print("--- Plan Generado ---")
            print(plan.steps[0].description)
            print("---------------------")
            
        # 3. Ejecución (LangChain AgentExecutor)
        try:
            response = self.executor.invoke({"input": user_input})
            return response["output"]
        except Exception as e:
            # Fallback en caso de error crítico del agente
            fallback_res = self.llm_provider.generate_response(user_input)
            return (
                "⚠️ **Contingencia Local Activa**\n\n"
                "El Agente ALI no pudo procesar la solicitud usando inteligencia artificial en la nube (se detectó un fallo en el proveedor de LLM).\n\n"
                f"{fallback_res}"
            )
