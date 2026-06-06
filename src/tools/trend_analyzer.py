from langchain_core.tools import tool
from src.infrastructure.database import SQLiteDatabaseAdapter
from src.config.settings import DB_PATH

@tool
def analizar_tendencias(sku: str, dias: int = 30) -> str:
    """
    Analiza las ventas históricas de un producto (SKU) en los últimos 'dias' días.
    Útil para calcular la venta diaria promedio y proyectar la demanda futura.
    """
    db = SQLiteDatabaseAdapter(DB_PATH)
    product = db.get_product(sku)
    if not product:
        return f"Error: No se encontró el producto con SKU {sku}."
        
    sales = db.get_sales_history(sku, dias)
    if not sales:
        return f"No hay registro de ventas para {sku} en los últimos {dias} días."
        
    total_vendido = sum(s.quantity for s in sales)
    venta_diaria_promedio = total_vendido / dias
    
    return f"""
    Análisis de Tendencias para {product.name} ({sku})
    Período analizado: Últimos {dias} días
    Total unidades vendidas: {total_vendido}
    Venta diaria promedio: {venta_diaria_promedio:.2f} unidades/día
    """
