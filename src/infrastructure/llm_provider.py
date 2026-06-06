import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from src.domain.interfaces import ILLMProvider
from src.infrastructure.database import SQLiteDatabaseAdapter
from src.config.settings import DB_PATH

class TripleFallbackLLMProvider(ILLMProvider):
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", 0.1))
        
        self.primary_llm = None
        self.fallback_llm = None
        
        self._initialize_providers()

    def _initialize_providers(self):
        if self.github_token and self.openai_base_url:
            self.primary_llm = ChatOpenAI(
                api_key=self.github_token,
                base_url=self.openai_base_url,
                model=self.model_name,
                temperature=self.temperature
            )
            
        if self.google_api_key:
            self.fallback_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=self.google_api_key,
                temperature=self.temperature
            )

    def generate_response(self, prompt: str) -> str:
        # Intento 1: Primary LLM (GitHub Models)
        if self.primary_llm:
            try:
                response = self.primary_llm.invoke(prompt)
                return response.content
            except Exception as e:
                print(f"[WARN] Falló el LLM primario (GitHub Models): {e}")
        
        # Intento 2: Fallback LLM (Gemini)
        if self.fallback_llm:
            try:
                print("[INFO] Usando LLM de respaldo (Gemini)")
                response = self.fallback_llm.invoke(prompt)
                return response.content
            except Exception as e:
                print(f"[WARN] Falló el LLM secundario (Gemini): {e}")

        # Intento 3: SQL Offline Fallback
        print("[CRITICAL] Usando Fallback SQL Offline.")
        return self._sql_offline_fallback(prompt)

    def _sql_offline_fallback(self, prompt: str) -> str:
        """
        Si todas las APIs fallan, proporcionamos respuestas heurísticas usando
        solo llamadas a la base de datos local SQLite.
        """
        db = SQLiteDatabaseAdapter(DB_PATH)
        
        # Heurística simple: si pregunta por inventario, stock, etc.
        if "stock" in prompt.lower() or "inventario" in prompt.lower() or "bajo" in prompt.lower():
            low_stock_items = db.get_low_stock_products()
            if not low_stock_items:
                return "[OFFLINE FALLBACK] Todos los productos tienen buen stock (>10)."
            
            res = "[OFFLINE FALLBACK] Productos con stock bajo crítico (<= 10):\n"
            for item in low_stock_items:
                prod = db.get_product(item.sku)
                name = prod.name if prod else "Desconocido"
                res += f"- {name} ({item.sku}): {item.stock_actual} unidades en {item.ubicacion}\n"
            return res
            
        return "[OFFLINE FALLBACK] APIs no disponibles. Solo puedo responder consultas básicas de stock bajo en este momento."

    def get_langchain_model(self):
        """Retorna el modelo LangChain principal con el fallback configurado nativamente si existe."""
        if self.primary_llm and self.fallback_llm:
            return self.primary_llm.with_fallbacks([self.fallback_llm])
        elif self.primary_llm:
            return self.primary_llm
        elif self.fallback_llm:
            return self.fallback_llm
        else:
            raise ValueError("No se configuró ningún LLM (GITHUB_TOKEN ni GOOGLE_API_KEY).")
