import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar la página
st.set_page_config(page_title="Análisis EnelGX", layout="wide")

# Cargar los datos
@st.cache_data
def load_data():
    df = pd.read_csv("enelgx_trimestre.csv", index_col=0)
    return df

df = load_data()

# Título principal
st.title("📊 Análisis Financiero de EnelGX")

# Selección de la métrica a visualizar
metric = st.selectbox("Selecciona una métrica:", df.index)

# Generar gráfico interactivo con Plotly
fig = px.line(df.T, y=metric, title=f"Evolución de {metric}", markers=True)
fig.update_layout(xaxis_title="Trimestres", yaxis_title=metric, xaxis_tickangle=270)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

# Mostrar la tabla de datos
st.subheader("📋 Datos")
st.dataframe(df.T)

# Agregar opción de descarga
st.download_button(
    label="📥 Descargar datos en CSV",
    data=df.T.to_csv().encode("utf-8"),
    file_name="enelgx_trimestre.csv",
    mime="text/csv"
)