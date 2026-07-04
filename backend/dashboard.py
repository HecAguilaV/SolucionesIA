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

# Estilo personalizado (Vanilla CSS/Streamlit)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background-color: #0f172a;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    }
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
            template="plotly_dark",
            color_discrete_sequence=["#38bdf8"]
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
                template="plotly_dark",
                color_continuous_scale="Viridis"
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
