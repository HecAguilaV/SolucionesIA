import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'omniretail.db')
CHROMA_PERSIST_DIR = os.path.join(DATA_DIR, 'chroma_store')
DOCS_DIR = os.path.join(DATA_DIR, 'docs')

# Asegurarse de que los directorios existan
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

# Configuración del Agente
AGENT_VERBOSE = os.getenv('AGENT_VERBOSE', 'true').lower() == 'true'
MEMORY_WINDOW_SIZE = int(os.getenv('MEMORY_WINDOW_SIZE', '10'))
