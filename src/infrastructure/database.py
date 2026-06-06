import sqlite3
from typing import List, Optional
from datetime import datetime, timedelta
from src.domain.entities import Product, InventoryStatus, SalesRecord
from src.domain.interfaces import IDatabaseAdapter
import os

class SQLiteDatabaseAdapter(IDatabaseAdapter):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        # Asegurarse de que el DB exista (si se corre desde distintos WDs)
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Base de datos no encontrada en {self.db_path}")
        return sqlite3.connect(self.db_path)

    def get_product(self, sku: str) -> Optional[Product]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
            row = cursor.fetchone()
            if row:
                return Product(sku=row[0], name=row[1], category=row[2], price=row[3], supplier_id=row[4], lead_time_days=row[5])
        return None

    def get_inventory_status(self, sku: str) -> Optional[InventoryStatus]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory WHERE sku = ?", (sku,))
            row = cursor.fetchone()
            if row:
                return InventoryStatus(sku=row[0], stock_actual=row[1], stock_transito=row[2], ubicacion=row[3])
        return None

    def get_sales_history(self, sku: str, days: int) -> List[SalesRecord]:
        target_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        sales = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sales WHERE sku = ? AND date >= ? ORDER BY date DESC", (sku, target_date))
            rows = cursor.fetchall()
            for row in rows:
                sales.append(SalesRecord(sku=row[1], date=datetime.strptime(row[2], '%Y-%m-%d'), quantity=row[3]))
        return sales

    def get_low_stock_products(self) -> List[InventoryStatus]:
        # Para el fallback SQL directo: retorna items con stock_actual <= 10
        low_stock = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory WHERE stock_actual <= 10")
            rows = cursor.fetchall()
            for row in rows:
                low_stock.append(InventoryStatus(sku=row[0], stock_actual=row[1], stock_transito=row[2], ubicacion=row[3]))
        return low_stock
