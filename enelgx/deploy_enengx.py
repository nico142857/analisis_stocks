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

st.title("Informacion ENELGXCH")

metric = st.selectbox("Selecciona una métrica:", df.index)

fig = px.line(df.T, y=metric, title=f"Evolución de {metric}", markers=True)
st.plotly_chart(fig, use_container_width=True)