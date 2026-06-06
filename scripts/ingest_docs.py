import os
from src.infrastructure.vector_store import ChromaDBVectorStoreAdapter
from src.config.settings import CHROMA_PERSIST_DIR, DOCS_DIR

def ingest_policy_documents():
    print(f"Iniciando ingesta de documentos desde {DOCS_DIR} a ChromaDB en {CHROMA_PERSIST_DIR}...")
    
    store = ChromaDBVectorStoreAdapter(persist_directory=CHROMA_PERSIST_DIR)
    
    documents = []
    ids = []
    metadatas = []
    
    # Leer todos los archivos .md en el directorio de documentos
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(DOCS_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Estrategia de chunking muy simple por secciones H2
            # Para un caso real usaríamos RecursiveCharacterTextSplitter de LangChain
            sections = content.split("## ")
            
            # El primer elemento puede ser el título principal
            title_part = sections[0].strip()
            
            for i, section in enumerate(sections[1:], 1):
                chunk_content = f"Contexto: {title_part}\n\n## {section.strip()}"
                chunk_id = f"{filename}_sec_{i}"
                
                documents.append(chunk_content)
                ids.append(chunk_id)
                metadatas.append({"source": filename, "section_index": i})
                
    if documents:
        store.ingest_documents(documents=documents, metadatas=metadatas, ids=ids)
        print(f"¡Éxito! Se ingestaron {len(documents)} fragmentos (chunks) de políticas en ChromaDB.")
    else:
        print("No se encontraron documentos para ingestar.")

if __name__ == "__main__":
    ingest_policy_documents()
