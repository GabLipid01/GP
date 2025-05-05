

# app.py

import streamlit as st
import pandas as pd

from data.profiles import FATTY_ACID_PROFILES
from data.sensory_esg_data import get_sensory_recipe, get_environmental_profile
from blend_calculator import calculate_blend_profile
from utils.visualizations import plot_fatty_acid_profile, show_pyramid, show_esg_panel
from utils.export_pdf import generate_pdf

# ==== CONFIGURAÇÃO DA PÁGINA ====
st.set_page_config(
    page_title="LipidGenesis - Blend LG",
    layout="wide",
    page_icon="🌿"
)

# ==== TÍTULO E INTRODUÇÃO ====
st.title("🌿 LipidGenesis - Bioengineering of Oils for Nextgen")
st.markdown(
    "<h4 style='text-align: center; color: #4C9B9C;'>"
    "Plataforma de Formulação Inteligente e Sensorial de Blends Lipídicos Sustentáveis"
    "</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# ==== SIDEBAR: INPUTS ====
st.sidebar.header("🧪 Parâmetros do Blend")

linha = st.sidebar.selectbox("Linha Sensorial", ["Vitalis", "Essentia", "Ardor", "Lúmina"])
ocasiao = st.sidebar.selectbox("Ocasião de Uso", ["Rosto", "Corpo", "Cabelos", "Banho"])

st.sidebar.markdown("### Composição (%) dos Óleos")
oil_percentages = {}
total_pct = 0

for oil in FATTY_ACID_PROFILES:
    pct = st.sidebar.slider(f"{oil}", 0, 100, 0, 1)
    oil_percentages[oil] = pct
    total_pct += pct

if total_pct == 0:
    st.warning("Defina pelo menos um óleo para gerar o blend.")
    st.stop()

# ==== CÁLCULO DO PERFIL LIPÍDICO ====
blend_profile = calculate_blend_profile(oil_percentages, FATTY_ACID_PROFILES)
df_lipid = pd.DataFrame.from_dict(blend_profile, orient="index", columns=["%"])
df_lipid.index.name = "Ácido Graxo"
df_lipid = df_lipid.sort_index()

# ==== EXIBIÇÃO DE DADOS ====
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Perfil Lipídico")
    st.dataframe(df_lipid.style.format({"%": "{:.2f}"}), height=400)

with col2:
    st.subheader("🧬 Visualização do Perfil")
    st.plotly_chart(plot_fatty_acid_profile(df_lipid), use_container_width=True)

# ==== COMPONENTE SENSORIAL ====
st.markdown("---")
st.subheader("🌸 Pirâmide Olfativa & Emoções Evocadas")
sensory_data = get_sensory_recipe(linha, ocasiao)
show_pyramid(sensory_data)

# ==== PAINEL AMBIENTAL E ESG ====
st.markdown("---")
st.subheader("🌱 Perfil Ambiental e ESG do Blend")
esg_data = get_environmental_profile(oil_percentages)
show_esg_panel(esg_data)

# ==== EXPORTAÇÃO ====
st.markdown("---")
if st.button("📄 Exportar PDF com Blend + Sensorial + ESG"):
    pdf_file = generate_pdf(
        blend_profile=blend_profile,
        oil_percentages=oil_percentages,
        sensory_data=sensory_data,
        esg_data=esg_data,
        linha=linha,
        ocasiao=ocasiao
    )
    st.success("Relatório gerado com sucesso!")
    st.download_button(
        label="📥 Baixar Relatório",
        data=pdf_file,
        file_name="LipidGenesis_Relatorio_Completo.pdf",
        mime="application/pdf"
    )

def calculate_blend_profile(percentages, profiles):
    total = sum(percentages.values())
    if total == 0:
        return {}

    normalized = {k: v / total for k, v in percentages.items()}
    all_acids = set()
    for p in profiles.values():
        all_acids.update(p.keys())

    result = {}
    for acid in sorted(all_acids):
        result[acid] = sum(
            normalized[oil] * profiles[oil].get(acid, 0)
            for oil in percentages
        )

    return result

FATTY_ACID_PROFILES = {
    "Palm Oil": {
        "C12:0": 0.2, "C14:0": 1.0, "C16:0": 44.0, "C16:1": 0.2,
        "C18:0": 4.5, "C18:1": 39.0, "C18:2": 10.0, "C18:3": 0.3,
        "C20:0": 0.2, "C20:1": 0.1
    },
    "Palm Olein": {
        "C12:0": 0.1, "C14:0": 1.0, "C16:0": 39.0, "C16:1": 0.2,
        "C18:0": 4.5, "C18:1": 43.5, "C18:2": 11.0, "C18:3": 0.3,
        "C20:0": 0.2, "C20:1": 0.2
    },
    "Palm Stearin": {
        "C14:0": 1.2, "C16:0": 56.0, "C16:1": 0.1, "C18:0": 6.5,
        "C18:1": 30.0, "C18:2": 5.0, "C18:3": 0.1, "C20:0": 0.3
    },
    "Palm Kernel Oil": {
        "C6:0": 0.2, "C8:0": 3.6, "C10:0": 3.5, "C12:0": 48.2,
        "C14:0": 16.2, "C16:0": 8.4, "C16:1": 0.1, "C18:0": 2.0,
        "C18:1": 15.3, "C18:2": 2.3, "C18:3": 0.1, "C20:0": 0.1
    }
}

def get_sensory_recipe(linha, ocasiao):
    base = {
        "Vitalis": {
            "topo": ["Capim-limão", "Alecrim"],
            "corpo": ["Lavanda", "Gerânio"],
            "fundo": ["Cedro", "Sândalo"],
            "emoções": ["Revigorante", "Equilíbrio"],
            "ícones": ["⚡", "🌿"]
        },
        "Essentia": {
            "topo": ["Bergamota", "Toranja"],
            "corpo": ["Ylang-Ylang", "Rosa"],
            "fundo": ["Patchouli", "Baunilha"],
            "emoções": ["Conforto", "Essência"],
            "ícones": ["✨", "🌸"]
        },
        "Ardor": {
            "topo": ["Pimenta rosa", "Cardamomo"],
            "corpo": ["Jasmim", "Cravo"],
            "fundo": ["Âmbar", "Madeira"],
            "emoções": ["Paixão", "Foco"],
            "ícones": ["❤️", "🔥"]
        },
        "Lúmina": {
            "topo": ["Mandarina", "Neroli"],
            "corpo": ["Lírio", "Magnólia"],
            "fundo": ["Almíscar", "Madeiras claras"],
            "emoções": ["Leveza", "Luz interior"],
            "ícones": ["☀️", "🕊️"]
        }
    }
    return base.get(linha, {})

def get_environmental_profile(percentages):
    impact_data = {
        "Palm Oil": {"impacto": 1.2, "origem": "Sustentável", "certificado": "RSPO"},
        "Palm Olein": {"impacto": 1.1, "origem": "Malásia", "certificado": "RSPO"},
        "Palm Stearin": {"impacto": 1.3, "origem": "Indonésia", "certificado": "RSPO"},
        "Palm Kernel Oil": {"impacto": 1.5, "origem": "Brasil", "certificado": "Orgânico"},
    }
    result = {}
    for oil, pct in percentages.items():
        data = impact_data.get(oil, {})
        result[oil] = {
            "Uso (%)": pct,
            "Impacto estimado": round(data.get("impacto", 1.0) * pct / 100, 2),
            "Origem": data.get("origem", "Desconhecida"),
            "Certificação": data.get("certificado", "Não informado"),
        }
    return result

import plotly.graph_objects as go
import streamlit as st

def plot_fatty_acid_profile(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index,
        y=df["%"],
        text=df["%"].map(lambda x: f"{x:.2f}%"),
        textposition="auto",
        marker_color="#4C9B9C"
    ))
    fig.update_layout(
        title="Distribuição de Ácidos Graxos",
        xaxis_title="Ácido Graxo",
        yaxis_title="Percentual (%)",
        template="simple_white"
    )
    return fig

def show_pyramid(data):
    st.markdown("#### Notas Olfativas")
    st.markdown(f"**Topo**: {', '.join(data['topo'])}")
    st.markdown(f"**Corpo**: {', '.join(data['corpo'])}")
    st.markdown(f"**Fundo**: {', '.join(data['fundo'])}")
    st.markdown("#### Emoções Evocadas")
    emotions = ", ".join(f"{i} {e}" for i, e in zip(data['ícones'], data['emoções']))
    st.markdown(f"{emotions}")

import streamlit as st
import pandas as pd

def show_esg_panel(data):
    df = pd.DataFrame.from_dict(data, orient="index")
    st.dataframe(df.style.format({
        "Uso (%)": "{:.1f}",
        "Impacto estimado": "{:.2f}"
    }), height=300)

from fpdf import FPDF
from io import BytesIO

def generate_pdf(blend_profile, oil_percentages, sensory_data, esg_data, linha, ocasiao):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório LipidGenesis", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Linha: {linha} | Ocasião: {ocasiao}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Perfil Lipídico", ln=True)
    pdf.set_font("Arial", "", 11)
    for acid, val in blend_profile.items():
        pdf.cell(0, 8, f"{acid}: {val:.2f}%", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Composição do Blend", ln=True)
    pdf.set_font("Arial", "", 11)
    for oil, pct in oil_percentages.items():
        pdf.cell(0, 8, f"{oil}: {pct:.1f}%", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Sensorial", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Topo: {', '.join(sensory_data['topo'])}", ln=True)
    pdf.cell(0, 8, f"Corpo: {', '.join(sensory_data['corpo'])}", ln=True)
    pdf.cell(0, 8, f"Fundo: {', '.join(sensory_data['fundo'])}", ln=True)
    pdf.cell(0, 8, f"Emoções: {', '.join(sensory_data['emoções'])}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Ambiental e ESG", ln=True)
    pdf.set_font("Arial", "", 11)
    for oil, data in esg_data.items():
        pdf.cell(0, 8, f"{oil}: {data['Impacto estimado']} impacto | Origem: {data['Origem']} | Cert.: {data['Certificação']}", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


