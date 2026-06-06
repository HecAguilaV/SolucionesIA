from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .entities import Product, InventoryStatus, SalesRecord, WeatherForecast

class IDatabaseAdapter(ABC):
    @abstractmethod
    def get_product(self, sku: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_inventory_status(self, sku: str) -> Optional[InventoryStatus]:
        pass

    @abstractmethod
    def get_sales_history(self, sku: str, days: int) -> List[SalesRecord]:
        pass
        
    @abstractmethod
    def get_low_stock_products(self) -> List[InventoryStatus]:
        pass

class IVectorStoreAdapter(ABC):
    @abstractmethod
    def similarity_search(self, query: str, k: int = 3) -> List[str]:
        pass

class ILLMProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass
