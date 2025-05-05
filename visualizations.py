import streamlit as st
import plotly.express as px

def plot_blend_pie(resultado):
    blend = resultado.get("Blend final", {})
    fig = px.pie(names=list(blend.keys()), values=list(blend.values()), title="Composição do Blend")
    st.plotly_chart(fig)

def show_pyramid(resultado):
    st.subheader("Pirâmide Olfativa (Simulada)")
    st.write("Notas de topo: coco")
    st.write("Notas de corpo: amendoado")
    st.write("Notas de fundo: terroso")