# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

from fpdf import FPDF
import tempfile
import matplotlib.pyplot as plt

def genera_grafico_pmv_ppd(pmv, ppd):
    """
    Genera il grafico PMV-PPD e lo restituisce come un file temporaneo.
    """
    import math
    pmv_values = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]
    ppd_values = [100 - 95 * math.exp(-0.03353 * x ** 4 - 0.2179 * x ** 2) for x in pmv_values]

    plt.figure(figsize=(6, 4))
    plt.plot(pmv_values, ppd_values, color='red', label="PPD (%)")
    plt.axhline(10, color='black', linestyle='--', label="PPD accettabile (10%)")
    plt.axvline(pmv, color='green', linestyle='--', label=f"PMV calcolato ({pmv:.2f})")
    plt.fill_between(pmv_values, 0, ppd_values, color="cyan", alpha=0.3)
    plt.scatter([pmv], [ppd], color='black')  # Punto calcolato
    plt.xlabel("PMV")
    plt.ylabel("PPD (%)")
    plt.title("Relazione tra PMV e PPD")
    plt.legend()
    plt.grid()

    # Salva il grafico in un file temporaneo
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_file.name)
    plt.close()
    return temp_file.name

def genera_report_pdf(temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento, pmv, ppd):
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
    return pdf_path
