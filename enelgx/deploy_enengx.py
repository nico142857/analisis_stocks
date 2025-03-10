import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv("enelgx_trimestre.csv", index_col=0)
    df = df.loc[:, ~df.columns.duplicated()].copy()
    df = df[~df.index.duplicated(keep='first')]
    return df

df = load_data()

st.title("Informacion Enel Generacion Chile")

metrics = st.multiselect("Selecciona métricas:", df.index, default=[df.index[0]])

fig = go.Figure()

if len(metrics) > 0:
    fig.add_trace(go.Scatter(
        x=df.T.index, y=df.T[metrics[0]],
        mode="lines+markers",
        name=metrics[0],
        yaxis="y1"
    ))

if len(metrics) > 1:
    fig.add_trace(go.Scatter(
        x=df.T.index, y=df.T[metrics[1]],
        mode="lines+markers",
        name=metrics[1],
        yaxis="y2"
    ))
    fig.update_layout(
        yaxis2=dict(
            title=metrics[1],
            overlaying="y",
            side="right",
            showgrid=False
        )
    )

fig.update_layout(
    title=f"Evolución de {', '.join(metrics)}",
    xaxis_title="Trimestres",
    yaxis=dict(title=metrics[0]),
    legend=dict(x=0, y=1),
    xaxis_tickangle=270
)

st.plotly_chart(fig, use_container_width=True)