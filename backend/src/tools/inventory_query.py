from langchain_core.tools import tool
from src.infrastructure.database import SQLiteDatabaseAdapter
from src.config.settings import DB_PATH
import sqlite3
from typing import Optional

@tool
def consultar_inventario(sku: Optional[str] = None) -> str:

    """
    Consulta el inventario de productos. 
    Si se provee un código SKU, muestra el detalle físico de ese producto específico.
    Si NO se provee un SKU (se deja en blanco o None), retorna la lista completa de todos los productos registrados y sus niveles de stock.
    """
    db = SQLiteDatabaseAdapter(DB_PATH)
    
    # Caso 1: No se especificó SKU -> Retornamos el inventario completo
    if not sku or sku.lower() in ["none", "all", "todos", ""]:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                query = """
                SELECT p.name, i.sku, i.stock_actual, i.stock_transito, i.ubicacion 
                FROM inventory i 
                JOIN products p ON i.sku = p.sku
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if not rows:
                    return "No hay productos registrados en el inventario actualmente."
                
                res = "📋 **Estado General del Inventario:**\n\n"
                for row in rows:
                    res += f"- **{row[0]}** (`{row[1]}`): {row[2]} uds. disponibles (En tránsito: {row[3]} uds.) en {row[4]}.\n"
                return res
        except Exception as e:
            return f"Error al recuperar el inventario general: {str(e)}"
            
    # Caso 2: Se especificó un SKU -> Buscamos el detalle del SKU específico
    product = db.get_product(sku)
    if not product:
        return f"Error: No se encontró el producto con SKU {sku}."
        
    inventory = db.get_inventory_status(sku)
    if not inventory:
        return f"Error: No se encontró registro de inventario para {sku}."
        
    return f"""
    Producto: {product.name} ({product.category})
    SKU: {sku}
    Stock Físico (Actual): {inventory.stock_actual}
    Stock en Tránsito: {inventory.stock_transito}
    Stock Total Disponible: {inventory.stock_total}
    Ubicación: {inventory.ubicacion}
    Lead Time (Días): {product.lead_time_days}
    """
