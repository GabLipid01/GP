from fpdf import FPDF

def exportar_pdf(resultado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório LipidGenesis", ln=True, align="C")
    for chave, valor in resultado.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)
    pdf.output("relatorio_blend.pdf")