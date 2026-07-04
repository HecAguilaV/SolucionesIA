from langchain_core.tools import tool
from src.infrastructure.database import SQLiteDatabaseAdapter
from src.config.settings import DB_PATH
from typing import Optional
from datetime import datetime, timedelta
import sqlite3

@tool
def analizar_tendencias(sku: Optional[str] = None, dias: int = 30) -> str:
    """
    Analiza las ventas históricas de los productos en los últimos 'dias' días.
    Si se provee un SKU, muestra el análisis detallado de ventas para ese producto específico.
    Si NO se provee un SKU (se deja en blanco o None), retorna un ranking de los productos más vendidos
    y la tendencia general de demanda del inventario.
    """
    db = SQLiteDatabaseAdapter(DB_PATH)
    target_date = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
    
    # Caso 1: Consulta general (sin SKU) -> Retorna el ranking de productos más vendidos
    if not sku or sku.lower() in ["none", "all", "todos", ""]:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                query = """
                SELECT p.name, s.sku, SUM(s.quantity) as total_vendido, AVG(s.quantity) as promedio_diario
                FROM sales s
                JOIN products p ON s.sku = p.sku
                WHERE s.date >= ?
                GROUP BY s.sku
                ORDER BY total_vendido DESC
                """
                cursor.execute(query, (target_date,))
                rows = cursor.fetchall()
                
                if not rows:
                    return f"No hay registros de ventas generales en los últimos {dias} días."
                
                res = f"📈 **Tendencias de Ventas y Demanda (Últimos {dias} días):**\n\n"
                for i, row in enumerate(rows, 1):
                    res += f"{i}. **{row[0]}** (`{row[1]}`): {row[2]} unidades vendidas (Promedio: {row[3]:.2f} uds/día)\n"
                return res
        except Exception as e:
            return f"Error al analizar las tendencias generales: {str(e)}"

    # Caso 2: Consulta específica por SKU
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
