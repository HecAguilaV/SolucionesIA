import os
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from src.domain.interfaces import IVectorStoreAdapter

class ChromaDBVectorStoreAdapter(IVectorStoreAdapter):
    def __init__(self, persist_directory: str, collection_name: str = "omniretail_policy"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Inicializar cliente ChromaDB
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def similarity_search(self, query: str, k: int = 3) -> List[str]:
        # Generar embedding para la query
        query_embedding = self.model.encode(query).tolist()
        
        # Buscar en la colección
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # Extraer los documentos recuperados
        documents = []
        if results and 'documents' in results and results['documents']:
            for doc_list in results['documents']:
                documents.extend(doc_list)
                
        return documents

    def ingest_documents(self, documents: List[str], metadatas: List[dict] = None, ids: List[str] = None):
        """Método utilitario para ingestar documentos en ChromaDB"""
        if not ids:
            ids = [f"doc_{i}" for i in range(len(documents))]
            
        embeddings = self.model.encode(documents).tolist()
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
