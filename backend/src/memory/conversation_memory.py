from langchain_classic.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_classic.base_memory import BaseMemory
from langchain_openai import ChatOpenAI
from src.config.settings import MEMORY_WINDOW_SIZE
import os

class MemoryManager:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL")
        self.model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
        
        self.llm = None
        if self.github_token and self.openai_base_url:
            self.llm = ChatOpenAI(
                api_key=self.github_token,
                base_url=self.openai_base_url,
                model=self.model_name,
                temperature=0.1
            )
            
    def get_window_memory(self, memory_key="chat_history") -> BaseMemory:
        """
        Retorna memoria de corto plazo basada en ventana (las últimas k interacciones).
        """
        return ConversationBufferWindowMemory(
            k=MEMORY_WINDOW_SIZE,
            memory_key=memory_key,
            return_messages=True
        )
        
    def get_summary_memory(self, memory_key="chat_history") -> BaseMemory:
        """
        Retorna memoria de largo plazo basada en resúmenes. Requiere un LLM configurado.
        """
        if not self.llm:
            print("[WARN] No hay LLM configurado para ConversationSummaryMemory. Usando WindowMemory como fallback.")
            return self.get_window_memory(memory_key=memory_key)
            
        return ConversationSummaryMemory(
            llm=self.llm,
            memory_key=memory_key,
            return_messages=True
        )
