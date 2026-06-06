from langchain_core.tools import tool
from src.memory.semantic_retriever import SemanticRetriever

@tool
def buscar_politicas_empresa(query: str) -> str:
    """
    Busca en los documentos internos de OmniRetail (políticas de inventario, 
    reglas de reposición, guías operativas) información relevante para tomar una decisión.
    Usa esta herramienta SIEMPRE antes de sugerir cantidades de reposición.
    """
    try:
        retriever = SemanticRetriever()
        return retriever.retrieve_policies(query)
    except Exception as e:
        return f"Error al consultar la base de conocimiento: {e}. Asume políticas estándar."
