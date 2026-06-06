from src.infrastructure.vector_store import ChromaDBVectorStoreAdapter
from src.config.settings import CHROMA_PERSIST_DIR
from typing import List

class SemanticRetriever:
    def __init__(self):
        self.store = ChromaDBVectorStoreAdapter(CHROMA_PERSIST_DIR)

    def retrieve_policies(self, query: str, k: int = 2) -> str:
        """
        Recupera y formatea las políticas más relevantes para una consulta.
        """
        documentos = self.store.similarity_search(query, k=k)
        
        if not documentos:
            return "No se encontró información relevante en las políticas internas."
            
        resultado = "Contexto recuperado de políticas de OmniRetail:\n\n"
        for i, doc in enumerate(documentos, 1):
            resultado += f"[{i}] {doc}\n\n"
            
        return resultado
