# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

from fpdf import FPDF
from grafici import genera_grafico_pmv_ppd
from spiegazioni_indici import spiegazioni_indici
import os
import datetime


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
    output_path="report_microclima.pdf",
    data=None,
):
    """
    Genera un report PDF con i risultati e il grafico PMV-PPD.
    """
    if data is None:
        data = datetime.date.today()
    grafico_path = genera_grafico_pmv_ppd(pmv, ppd)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, txt="Analisi del Microclima Ufficio", ln=True, align="C")
    pdf.ln(3)
    pdf.set_font("Arial", size=10)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Informazioni generali
    pdf.cell(60, 8, txt=f"Sede: {sede}", border=0)
    pdf.cell(80, 8, txt=f"Descrizione: {descrizione_locale}", border=0)
    pdf.cell(50, 8, txt=f"Data: {data}", ln=True)
    pdf.ln(3)

    # Parametri ambientali
    pdf.cell(0, 8, txt="Parametri ambientali:", ln=True)

    labels = [
        "Temperatura aria (°C):",
        "Temperatura radiante (°C):",
        "Velocità aria (m/s):",
        "Umidità relativa (%):",
        "Metabolismo (Met):",
        "Isolamento termico (Clo):",
        "Sede:",
        "Descrizione del locale:",
    ]
    values = [
        temp_aria,
        temp_radiante,
        vel_aria,
        umidita,
        metabolismo,
        isolamento,
        sede,
        descrizione_locale,
    ]

    for label, value in zip(labels, values):
        pdf.cell(95, 8, txt=label, border=0)
        pdf.cell(95, 8, txt=str(value), ln=True)

    pdf.ln(5)

    # Risultati
    pdf.cell(0, 8, txt="Risultati calcolati:", ln=True)
    pdf.cell(95, 8, txt="Indice PMV:")
    pdf.cell(95, 8, txt=f"{pmv:.2f}", ln=True)
    pdf.cell(95, 8, txt="Indice PPD:")
    pdf.cell(95, 8, txt=f"{ppd:.2f}%", ln=True)
    pdf.multi_cell(0, 8, txt=spiegazioni_indici["pmv"])
    pdf.ln(1)
    pdf.multi_cell(0, 8, txt=spiegazioni_indici["ppd"])
    pdf.ln(5)

    # Nuova pagina per il grafico
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, txt="Grafico PMV-PPD", ln=True, align="C")
    pdf.ln(3)
    pdf.set_font("Arial", size=10)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Inserimento del grafico nel PDF
    pdf.cell(0, 8, txt="Grafico PMV-PPD:", ln=True)
    image_x = (pdf.w - 130) / 2
    image_y = pdf.get_y() + 5
    pdf.image(grafico_path, x=image_x, y=image_y, w=130)
    pdf.set_y(image_y + 87)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, txt="Commenti del responsabile:", ln=True)
    comment_y = pdf.get_y()
    pdf.rect(10, comment_y, 190, 25)
    pdf.ln(28)
    pdf.cell(0, 8, txt="Firma del responsabile: ____________________", ln=True)

    # Salva il PDF
    pdf.output(output_path)

    # Rimuove il file temporaneo del grafico
    try:
        os.remove(grafico_path)
    except OSError:
        pass

    return output_path
