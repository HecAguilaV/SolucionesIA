from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Product:
    sku: str
    name: str
    category: str
    price: float
    supplier_id: str
    lead_time_days: int

@dataclass
class InventoryStatus:
    sku: str
    stock_actual: int
    stock_transito: int
    ubicacion: str
    
    @property
    def stock_total(self) -> int:
        return self.stock_actual + self.stock_transito

@dataclass
class SalesRecord:
    sku: str
    date: datetime
    quantity: int

@dataclass
class WeatherForecast:
    date: datetime
    temperature: float
    condition: str
    is_alert: bool = False

@dataclass
class RecommendationResult:
    sku: str
    action: str  # e.g., 'REORDER', 'HOLD', 'URGENT_REORDER'
    quantity_suggested: int
    justification: str
    context_used: List[str] = field(default_factory=list)
