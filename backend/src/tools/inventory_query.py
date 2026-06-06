from langchain_core.tools import tool
from src.infrastructure.database import SQLiteDatabaseAdapter
from src.config.settings import DB_PATH

@tool
def consultar_inventario(sku: str) -> str:
    """
    Consulta el inventario actual de un producto por su código SKU.
    Útil cuando necesitas saber cuánto stock físico hay de un producto.
    """
    db = SQLiteDatabaseAdapter(DB_PATH)
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
