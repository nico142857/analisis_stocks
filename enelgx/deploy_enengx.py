import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("enelgx_trimestre.csv", index_col=0)
    df = df.loc[:, ~df.columns.duplicated()].copy()
    df = df[~df.index.duplicated(keep='first')]
    return df

df = load_data()

st.title("Informacion EnelGXCH")

metrics = st.multiselect("Selecciona métricas:", df.index, default=[df.index[0]])

fig = px.line(df.T, y=metrics, title=f"Evolución de {', '.join(metrics)}", markers=True)

st.plotly_chart(fig, use_container_width=True)