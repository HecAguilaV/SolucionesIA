from langchain_core.tools import tool
import os
from datetime import datetime
from src.config.settings import DATA_DIR

@tool
def escribir_reporte(titulo: str, contenido: str) -> str:
    """
    Escribe un reporte oficial con las recomendaciones de inventario y lo guarda en disco.
    Útil como paso final después de analizar datos y tomar una decisión.
    """
    try:
        reportes_dir = os.path.join(DATA_DIR, 'reportes')
        os.makedirs(reportes_dir, exist_ok=True)
        
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_{titulo.replace(' ', '_').lower()}_{fecha}.md"
        filepath = os.path.join(reportes_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {titulo}\n")
            f.write(f"**Fecha de generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(contenido)
            
        return f"Reporte guardado exitosamente en: {filepath}"
    except Exception as e:
        return f"Error al guardar el reporte: {e}"
