import sqlite3
import random
from datetime import datetime, timedelta
import os

# Asegurarse de que el directorio data exista
os.makedirs('data', exist_ok=True)
DB_PATH = 'data/omniretail.db'

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla de Productos (SKUs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            supplier_id TEXT NOT NULL,
            lead_time_days INTEGER NOT NULL
        )
    ''')

    # Tabla de Inventario Físico
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            sku TEXT PRIMARY KEY,
            stock_actual INTEGER NOT NULL,
            stock_transito INTEGER NOT NULL,
            ubicacion TEXT NOT NULL,
            FOREIGN KEY (sku) REFERENCES products(sku)
        )
    ''')

    # Tabla de Ventas Históricas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL,
            date DATE NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (sku) REFERENCES products(sku)
        )
    ''')

    # Insertar Productos Base
    products = [
        ('SKU-1001', 'Bloqueador Solar FPS 50', 'Estacional', 12.99, 'SUP-001', 5),
        ('SKU-1002', 'Bebida Isotónica 500ml', 'Alta Rotación', 1.50, 'SUP-002', 2),
        ('SKU-1003', 'Ventilador de Pie', 'Estacional', 45.00, 'SUP-003', 10),
        ('SKU-1004', 'Paraguas Compacto', 'Estacional', 8.50, 'SUP-004', 7),
        ('SKU-1005', 'Smart TV 55"', 'Electrónica', 350.00, 'SUP-005', 15),
        ('SKU-1006', 'Sopa Instantánea', 'Alimentos perecederos', 0.99, 'SUP-002', 3),
        ('SKU-1007', 'Detergente Líquido 3L', 'Alta Rotación', 9.50, 'SUP-001', 4),
        ('SKU-1008', 'Parca Impermeable Térmica', 'Estacional', 89.99, 'SUP-004', 8)
    ]
    cursor.executemany('INSERT OR REPLACE INTO products VALUES (?,?,?,?,?,?)', products)

    # Insertar Inventario Base (situaciones variadas para que el agente reaccione)
    inventory = [
        ('SKU-1001', 8, 0, 'Viña del Mar'),    # Stock crítico (antes 25)
        ('SKU-1002', 500, 100, 'Santiago'),    # Buen stock
        ('SKU-1003', 5, 0, 'Santiago'),        # Quiebre inminente
        ('SKU-1004', 120, 0, 'Concepción'),    # Stock normal
        ('SKU-1005', 48, 5, 'Santiago'),       # Stock límite electrónica
        ('SKU-1006', 200, 50, 'Viña del Mar'), # Stock normal
        ('SKU-1007', 3, 0, 'Concepción'),      # Stock crítico (antes 45)
        ('SKU-1008', 4, 10, 'Temuco')          # Stock crítico nuevo
    ]
    cursor.executemany('INSERT OR REPLACE INTO inventory VALUES (?,?,?,?)', inventory)

    # Generar ~500 registros de ventas de los últimos 30 días
    sales_data = []
    base_date = datetime.now() - timedelta(days=30)
    
    for _ in range(500):
        sku = random.choice([p[0] for p in products])
        days_offset = random.randint(0, 29)
        sale_date = (base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        
        # Volúmenes variados
        if '1005' in sku: # TV
            qty = random.randint(1, 3)
        elif '1002' in sku or '1006' in sku: # Bebidas, Sopas
            qty = random.randint(10, 50)
        else:
            qty = random.randint(2, 15)
            
        sales_data.append((sku, sale_date, qty))

    # Limpiar ventas anteriores e insertar nuevas
    cursor.execute('DELETE FROM sales')
    cursor.executemany('INSERT INTO sales (sku, date, quantity) VALUES (?,?,?)', sales_data)

    conn.commit()
    conn.close()
    print(f"Base de datos SQLite generada con éxito en {DB_PATH}")
    print(f"Productos insertados: {len(products)}")
    print(f"Registros de ventas generados: {len(sales_data)}")

if __name__ == '__main__':
    create_database()
