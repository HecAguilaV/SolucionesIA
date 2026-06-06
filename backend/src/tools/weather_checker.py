from langchain_core.tools import tool
import random
from datetime import datetime, timedelta

@tool
def consultar_clima(ciudad: str) -> str:
    """
    Consulta el pronóstico del clima a 7 días para una ciudad específica (ej: 'Santiago', 'Viña del Mar').
    Esencial para prever picos de demanda en productos estacionales debido a olas de calor o frío.
    """
    # Simulador de clima ya que no usamos API externa de clima para mantenerlo simple.
    # Pero da respuestas determinísticas para las ciudades de nuestras tiendas.
    
    ciudad = ciudad.lower().strip()
    dias = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    
    if "santiago" in ciudad:
        # Simulamos una ola de calor en Santiago
        clima = f"Pronóstico para Santiago:\n"
        clima += f"- {dias[0]}: 33°C (Soleado, ALERTA OLA DE CALOR)\n"
        clima += f"- {dias[1]}: 35°C (Soleado, ALERTA OLA DE CALOR)\n"
        clima += f"- {dias[2]}: 34°C (Soleado, ALERTA OLA DE CALOR)\n"
        clima += f"- {dias[3]}: 30°C (Soleado)\n"
        clima += f"- Resto de la semana: ~28°C\n"
        return clima
        
    elif "viña" in ciudad or "valparaiso" in ciudad:
        # Simulamos clima normal
        clima = f"Pronóstico para Viña del Mar:\n"
        clima += f"- {dias[0]} al {dias[6]}: Promedio 22°C (Mayormente nublado, típico de la costa)\n"
        return clima
        
    elif "concepción" in ciudad:
        # Simulamos lluvias
        clima = f"Pronóstico para Concepción:\n"
        clima += f"- {dias[0]} al {dias[2]}: 15°C (Lluvia fuerte, ALERTA FRENTE FRÍO)\n"
        clima += f"- {dias[3]} al {dias[6]}: 18°C (Parcialmente nublado)\n"
        return clima
        
    else:
        return f"Pronóstico para {ciudad}: Clima templado normal, sin alertas climáticas."
