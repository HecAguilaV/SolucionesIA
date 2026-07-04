import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from datetime import datetime
import streamlit.components.v1 as components

# Auto-refresh cada 60 segundos
components.html(
    """
    <script>
        setTimeout(function() {
            window.parent.location.reload();
        }, 60000);
    </script>
    """,
    height=0
)

# Configuración de página
st.set_page_config(
    page_title="OmniRetail ALI - Observabilidad",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Selector de Tema
st.sidebar.subheader("Personalización")
selected_theme = st.sidebar.selectbox(
    "Tema Visual:",
    ["Oscuro Slate", "Clarito Corporativo"]
)

# Configuración de Colores y Plantillas
theme_config = {
    "Oscuro Slate": {
        "bg_color": "#0f172a",
        "sidebar_bg_color": "#1e293b",
        "sidebar_text_color": "#f1f5f9",
        "card_bg_color": "#1e293b",
        "card_border_color": "#334155",
        "text_color": "#f1f5f9",
        "accent_color": "#38bdf8",
        "plotly_template": "plotly_dark",
        "color_scale": "Viridis"
    },
    "Clarito Corporativo": {
        "bg_color": "#f8fafc",
        "sidebar_bg_color": "#e2e8f0",
        "sidebar_text_color": "#0f172a",
        "card_bg_color": "#ffffff",
        "card_border_color": "#e2e8f0",
        "text_color": "#0f172a",
        "accent_color": "#0284c7",
        "plotly_template": "plotly_white",
        "color_scale": "Blues"
    }
}

cfg = theme_config[selected_theme]

# Inyección de CSS dinámico avanzado para redefinir variables de Streamlit y forzar contraste
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Redefinir variables CSS globales de Streamlit */
    :root, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {{
        --text-color: {cfg["text_color"]} !important;
        --background-color: {cfg["bg_color"]} !important;
        --secondary-background-color: {cfg["sidebar_bg_color"]} !important;
        --primary-color: {cfg["accent_color"]} !important;
    }}
    
    /* Forzar fondo general y cabecera */
    .stApp, [data-testid="stHeader"], header {{
        background-color: {cfg["bg_color"]} !important;
        color: {cfg["text_color"]} !important;
    }}
    
    /* Forzar fondo de las tarjetas de métricas */
    .stMetric {{
        background-color: {cfg["card_bg_color"]} !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid {cfg["card_border_color"]} !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1) !important;
    }}

    /* Estilos específicos de la barra lateral (Sidebar) */
    [data-testid="stSidebar"] {{
        background-color: {cfg["sidebar_bg_color"]} !important;
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {{
        color: {cfg["sidebar_text_color"]} !important;
    }}

    /* Forzar estilos en listas desplegables (selectboxes y multiselects) y menús flotantes */
    div[data-baseweb="select"] > div, div[role="listbox"], ul[role="listbox"], li[role="option"] {{
        background-color: {cfg["card_bg_color"]} !important;
        color: {cfg["text_color"]} !important;
        border-color: {cfg["card_border_color"]} !important;
    }}

    /* Estilos de botones generales */
    .stButton > button {{
        background-color: {cfg["card_bg_color"]} !important;
        color: {cfg["text_color"]} !important;
        border: 1px solid {cfg["card_border_color"]} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Ruta del archivo de logs
LOG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../data/agent_observability.jsonl"
)

# Cargar logs
def load_data():
    if not os.path.exists(LOG_FILE_PATH):
        return pd.DataFrame()
    
    data = []
    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except Exception:
                    pass
    
    if not data:
        return pd.DataFrame()
        
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp", ascending=False)
    return df

st.title(":material/monitoring: OmniRetail ALI — Panel de Control & Observabilidad")
st.markdown("Monitoreo en tiempo real del Agente de Logística Inteligente.")

df = load_data()

if df.empty:
    st.info("Aún no se registran interacciones en el Agente ALI. ¡Realizá tu primera consulta en el chat!")
else:
    # Sidebar controles y filtros
    st.sidebar.header("Controles")
    if st.sidebar.button("🔄 Actualizar Datos"):
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtros del Sistema")
    status_filter = st.sidebar.multiselect(
        "Estado de la Solicitud:",
        options=df["status"].unique(),
        default=df["status"].unique()
    )
    
    filtered_df = df[df["status"].isin(status_filter)]
    
    # Calcular métricas clave
    total_requests = len(filtered_df)
    success_rate = (filtered_df["status"] == "success").sum() / total_requests * 100 if total_requests > 0 else 0.0
    avg_latency = filtered_df["latency_sec"].mean() if total_requests > 0 else 0.0
    total_tokens = filtered_df["tokens_estimated"].sum() if total_requests > 0 else 0
    avg_accuracy = filtered_df["accuracy_eval"].dropna().mean() if total_requests > 0 and not filtered_df["accuracy_eval"].dropna().empty else 100.0

    # Fila de KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Consultas Totales", f"{total_requests}")
    col2.metric("Tasa de Éxito", f"{success_rate:.1f}%")
    col3.metric("Latencia Promedio", f"{avg_latency:.2f} s")
    col4.metric("Tokens Estimados", f"{total_tokens:,}")
    col5.metric("Precisión LLM Eval", f"{avg_accuracy:.1f}/100")

    # Gráficos e Insights
    st.markdown("---")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("### :material/speed: Latencia en el Tiempo (s)")
        fig_lat = px.line(
            filtered_df,
            x="timestamp",
            y="latency_sec",
            markers=True,
            labels={"timestamp": "Fecha y Hora", "latency_sec": "Latencia (s)"},
            template=cfg["plotly_template"],
            color_discrete_sequence=[cfg["accent_color"]]
        )
        # Forzar fondo transparente en Plotly para que herede el fondo de la app
        fig_lat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=cfg["text_color"]
        )
        st.plotly_chart(fig_lat, use_container_width=True)

    with col_g2:
        st.markdown("### :material/construction: Distribución de Herramientas Usadas")
        # Aplanar lista de herramientas
        all_tools = []
        for tools_list in filtered_df["tools_used"]:
            all_tools.extend(tools_list)
        
        if all_tools:
            tools_df = pd.Series(all_tools).value_counts().reset_index()
            tools_df.columns = ["Herramienta", "Invocaciones"]
            fig_tools = px.bar(
                tools_df,
                x="Invocaciones",
                y="Herramienta",
                orientation="h",
                color="Invocaciones",
                template=cfg["plotly_template"],
                color_continuous_scale=cfg["color_scale"]
            )
            # Forzar fondo transparente en Plotly para que herede el fondo de la app
            fig_tools.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color=cfg["text_color"]
            )
            st.plotly_chart(fig_tools, use_container_width=True)
        else:
            st.info("No se han invocado herramientas en el rango seleccionado (modo fallback o consultas generales).")

    st.markdown("---")
    st.markdown("### :material/database: Historial Detallado de Trazabilidad (Logs)")
    
    # Formatear visualización
    display_df = filtered_df.copy()
    display_df["timestamp"] = display_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    st.dataframe(
        display_df[["timestamp", "query", "response", "latency_sec", "status", "tools_used", "accuracy_eval"]],
        use_container_width=True
    )
