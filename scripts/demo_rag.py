import os
import sys
import argparse
from dotenv import load_dotenv

# Asegurar que la raíz del proyecto esté en el PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.memory.semantic_retriever import SemanticRetriever
from src.infrastructure.llm_provider import TripleFallbackLLMProvider

def run_rag_demo(query: str, k: int = 3):
    print("======================================================================")
    print("🔍 INICIANDO PIPELINE RAG - OMNIRETAIL S.A.")
    print(f"Pregunta: '{query}'")
    print("======================================================================\n")

    # 1. Recuperación Semántica (RAG)
    print("1️⃣ Recuperando contexto relevante de ChromaDB...")
    retriever = SemanticRetriever()
    context = retriever.retrieve_policies(query, k=k)
    print("\n--- [CONTEXTO RECUPERADO] ---")
    print(context)
    print("-------------------------------\n")

    # 2. Inicialización del LLM
    print("2️⃣ Inicializando proveedor de LLM con fallbacks...")
    try:
        llm = TripleFallbackLLMProvider()
    except Exception as e:
        print(f"❌ Error al inicializar el LLM: {e}")
        return

    # 3. Construcción del Prompt Enriquecido
    system_prompt = f"""Eres ALI (Agente de Logística Inteligente) de OmniRetail S.A.
Tu rol es asistir a los jefes de tienda en consultas sobre stock, tendencias y políticas de reposición.

Debes responder a la consulta del usuario basándote estrictamente en el siguiente contexto recuperado de las políticas y guías de la empresa.
Si no puedes encontrar la respuesta en el contexto, indica amablemente que no posees esa información.

---
CONTEXTO DE POLÍTICAS VIGENTES:
{context}
---
"""
    full_prompt = f"{system_prompt}\n\nConsulta del usuario: {query}\nRespuesta:"

    # 4. Generación de Respuesta
    print("3️⃣ Generando respuesta con el LLM...")
    response = llm.generate_response(full_prompt)
    
    print("\n--- [RESPUESTA DEL AGENTE] ---")
    print(response)
    print("-------------------------------\n")

if __name__ == "__main__":
    load_dotenv()
    
    # Si no hay tokens configurados, advertir al usuario
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GITHUB_TOKEN"):
        print("⚠️  ADVERTENCIA: No se detecta GOOGLE_API_KEY ni GITHUB_TOKEN en el entorno.")
        print("Se usará el modo SQL Offline Fallback por defecto.\n")

    parser = argparse.ArgumentParser(description="Demo del Pipeline RAG para la Evaluación 1")
    parser.add_argument("--query", type=str, default="¿Cuál es la política para quiebres de stock y alertas de reposición?", 
                        help="Consulta en lenguaje natural sobre las políticas corporativas")
    parser.add_argument("-k", type=int, default=2, help="Número de fragmentos a recuperar de ChromaDB")
    
    args = parser.parse_args()
    run_rag_demo(args.query, args.k)
