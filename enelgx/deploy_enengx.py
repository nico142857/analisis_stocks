import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "enelgx_trimestre.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(file_path, index_col=0)
    df = df.loc[:, ~df.columns.duplicated()].copy()
    df = df[~df.index.duplicated(keep='first')]
    return df

df = load_data()

st.title("Información Enel Generación Chile")

# Crear tres gráficos individuales para métricas clave
key_metrics = ["Ingresos ($M)", "Utilidad controladora ($M)", "FCF ($M)"]
for metric in key_metrics:
    if metric in df.index:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df.T.index, y=df.T[metric],
            name=metric
        ))
        fig.update_layout(
            title=f"Evolución de {metric}",
            xaxis_title="Trimestres",
            yaxis_title=metric,
            xaxis_tickangle=270
        )
        st.plotly_chart(fig, use_container_width=True)

# Sección interactiva con selección de métricas
metrics = st.multiselect("Selecciona métricas:", df.index, default=[df.index[0]])

fig = go.Figure()

if len(metrics) > 0:
    fig.add_trace(go.Bar(
        x=df.T.index, y=df.T[metrics[0]],
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
    xaxis_tickangle=270,
    barmode='group'  # To group bars when multiple metrics are selected
)

st.plotly_chart(fig, use_container_width=True)
