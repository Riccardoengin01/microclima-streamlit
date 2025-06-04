# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

from fpdf import FPDF
from grafici import genera_grafico_pmv_ppd
import os

def genera_report_pdf(
    temp_aria,
    temp_radiante,
    vel_aria,
    umidita,
    metabolismo,
    isolamento,
    pmv,
    ppd,
    sede,
    descrizione_locale,
):
    """
    Genera un report PDF con i risultati e il grafico PMV-PPD.
    """
    grafico_path = genera_grafico_pmv_ppd(pmv, ppd)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Analisi del Microclima Ufficio", ln=True, align='C')
    pdf.ln(10)

    # Parametri ambientali
    pdf.cell(200, 10, txt="Parametri ambientali:", ln=True)
    pdf.cell(200, 10, txt=f"Temperatura aria (°C): {temp_aria}", ln=True)
    pdf.cell(200, 10, txt=f"Temperatura radiante (°C): {temp_radiante}", ln=True)
    pdf.cell(200, 10, txt=f"Velocità aria (m/s): {vel_aria}", ln=True)
    pdf.cell(200, 10, txt=f"Umidità relativa (%): {umidita}", ln=True)
    pdf.cell(200, 10, txt=f"Metabolismo (Met): {metabolismo}", ln=True)
    pdf.cell(200, 10, txt=f"Isolamento termico (Clo): {isolamento}", ln=True)
    pdf.cell(200, 10, txt=f"Sede: {sede}", ln=True)
    pdf.cell(200, 10, txt=f"Descrizione del locale: {descrizione_locale}", ln=True)
    pdf.ln(10)

    # Risultati
    pdf.cell(200, 10, txt="Risultati calcolati:", ln=True)
    pdf.cell(200, 10, txt=f"Indice PMV: {pmv:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Indice PPD: {ppd:.2f}%", ln=True)
    pdf.ln(10)

    # Inserimento del grafico nel PDF
    pdf.cell(200, 10, txt="Grafico PMV-PPD:", ln=True)
    pdf.image(grafico_path, x=10, y=pdf.get_y() + 10, w=150)
    pdf.ln(85)

    # Salva il PDF
    pdf_path = "report_microclima.pdf"
    pdf.output(pdf_path)

    # Rimuove il file temporaneo del grafico
    try:
        os.remove(grafico_path)
    except OSError:
        pass

    return pdf_path
