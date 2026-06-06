import streamlit as st
from src.application.agent import InventoryAgent
import os
import sqlite3
import pandas as pd
from src.config.settings import DB_PATH

# Configuración de página
st.set_page_config(
    page_title="Agente de Inventario - OmniRetail",
    page_icon="🤖",
    layout="wide"
)

# Inicializar agente en session_state para mantener la memoria
if "agent" not in st.session_state:
    with st.spinner("Inicializando agente inteligente..."):
        st.session_state.agent = InventoryAgent()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hola, soy tu Agente de Gestión de Inventario OmniRetail. ¿En qué te puedo ayudar hoy?"}
    ]

# Función auxiliar para ver estado de la BD
def ver_stock_critico():
    try:
        conn = sqlite3.connect(DB_PATH)
        query = """
        SELECT p.name as Producto, i.sku as SKU, i.stock_actual as Stock, i.ubicacion as Ubicación 
        FROM inventory i 
        JOIN products p ON i.sku = p.sku 
        WHERE i.stock_actual <= 10
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

# Sidebar
with st.sidebar:
    st.title("📊 Panel de Control OmniRetail")
    st.markdown("---")
    st.subheader("Estado del Sistema")
    
    # Check APIs
    has_github = bool(os.getenv("GITHUB_TOKEN"))
    has_gemini = bool(os.getenv("GOOGLE_API_KEY"))
    
    st.write(f"GitHub Models API: {'✅' if has_github else '❌'}")
    st.write(f"Google Gemini API: {'✅' if has_gemini else '❌'}")
    
    if not (has_github or has_gemini):
        st.error("Modo Offline Activo: Se usarán fallbacks SQL básicos.")
        
    st.markdown("---")
    st.subheader("⚠️ Alertas Críticas (Stock <= 10)")
    df_critico = ver_stock_critico()
    if not df_critico.empty:
        st.dataframe(df_critico, hide_index=True)
    else:
        st.success("No hay productos con stock crítico.")
        
    st.markdown("---")
    st.caption("Evaluación Parcial 2 - ISY0101")

# Main layout
st.title("🤖 Chat Assistant")

# Mostrar historial de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input de usuario
if prompt := st.chat_input("Ej: ¿Cuál es el stock actual del bloqueador solar?"):
    # Añadir a UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Procesar con agente
    with st.chat_message("assistant"):
        with st.spinner("Analizando y planificando..."):
            response = st.session_state.agent.process_request(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
