# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

from fpdf import FPDF
from grafici import (
    genera_grafico_pmv_ppd,
    genera_grafico_pmv_ppd_avanzato,
    genera_grafico_lux_db,
)
from spiegazioni_indici import spiegazioni_indici, spiegazioni_indici_en
from traduzioni import LABELS
import os
import datetime


class PdfGenerationError(Exception):
    """Errore durante la generazione del report PDF."""


def genera_report_pdf(
    temp_aria,
    temp_radiante,
    vel_aria,
    umidita,
    illuminazione,
    impatto_acustico,
    metabolismo,
    isolamento,
    pmv,
    ppd,
    sede,
    descrizione_locale,
    commento_responsabile="",
    firma_responsabile="",
    output_path="report_microclima.pdf",
    data=None,
    lingua="it",
):
    """
    Genera un report PDF con i risultati e tre grafici riepilogativi.
    """
    if data is None:
        data = datetime.date.today()
    grafico_path = genera_grafico_pmv_ppd(pmv, ppd)
    grafico_avanzato_path = genera_grafico_pmv_ppd_avanzato(
        pmv, ppd, temp_aria, umidita
    )
    grafico_lux_db_path = genera_grafico_lux_db(illuminazione, impatto_acustico)
    testi = LABELS[lingua]
    spiegazioni = spiegazioni_indici if lingua == "it" else spiegazioni_indici_en

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, txt=testi["title"], ln=True, align="C")
    pdf.ln(3)
    pdf.set_font("Arial", size=10)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Informazioni generali
    pdf.cell(60, 8, txt=f"{testi['location']}: {sede}", border=0)
    pdf.cell(80, 8, txt=f"{testi['description']}: {descrizione_locale}", border=0)
    pdf.cell(50, 8, txt=f"{testi['date']}: {data}", ln=True)
    pdf.ln(3)

    # Parametri ambientali
    pdf.cell(0, 8, txt=testi["sidebar_header"] + ":", ln=True)

    labels = [
        testi["air_temp"],
        testi["rad_temp"],
        testi["air_speed"],
        testi["humidity"],
        testi["metabolism"],
        testi["insulation"],
        testi["lighting"],
        testi["noise"],
        testi["location"] + ":",
        testi["description"] + ":",
    ]
    values = [
        temp_aria,
        temp_radiante,
        vel_aria,
        umidita,
        metabolismo,
        isolamento,
        illuminazione,
        impatto_acustico,
        sede,
        descrizione_locale,
    ]

    for label, value in zip(labels, values):
        pdf.cell(95, 8, txt=label, border=0)
        pdf.cell(95, 8, txt=str(value), ln=True)

    pdf.ln(5)

    # Risultati
    pdf.cell(0, 8, txt=testi["results"] + ":", ln=True)
    pdf.cell(95, 8, txt=testi["pmv"])
    pdf.cell(95, 8, txt=f"{pmv:.2f}", ln=True)
    pdf.cell(95, 8, txt=testi["ppd"])
    pdf.cell(95, 8, txt=f"{ppd:.2f}%", ln=True)
    pdf.multi_cell(0, 8, txt=spiegazioni["pmv"])
    pdf.ln(1)
    pdf.multi_cell(0, 8, txt=spiegazioni["ppd"])
    pdf.ln(5)

    # Nuova pagina per il grafico
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, txt="Grafici PMV-PPD", ln=True, align="C")
    pdf.ln(3)
    pdf.set_font("Arial", size=10)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Inserimento dei grafici nel PDF
    pdf.cell(0, 8, txt="Grafici:", ln=True)
    image_w = 90
    image_y = pdf.get_y() + 5
    pdf.image(grafico_path, x=10, y=image_y, w=image_w)
    pdf.image(grafico_avanzato_path, x=110, y=image_y, w=image_w)
    pdf.set_y(image_y + 70)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, txt="Commenti del responsabile:", ln=True)
    if commento_responsabile:
        pdf.multi_cell(0, 8, txt=commento_responsabile)
    else:
        pdf.ln(8)
    pdf.cell(
        0,
        8,
        txt=f"Firma del responsabile: {firma_responsabile}",
        ln=True,
    )
    pdf.ln(20)

    space_left = pdf.h - pdf.b_margin - pdf.get_y()
    if space_left < 125:
        pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, txt="Illuminazione e Rumore", ln=True, align="C")
    pdf.ln(3)
    pdf.set_font("Arial", size=10)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    image_w = 100
    image_x = (pdf.w - image_w) / 2
    image_y = pdf.get_y() + 5
    pdf.image(grafico_lux_db_path, x=image_x, y=image_y, w=image_w)
    pdf.set_y(image_y + 70)

    # Salva il PDF
    try:
        pdf.output(output_path)
    except (IOError, OSError) as exc:
        raise PdfGenerationError(f"Impossibile scrivere il file {output_path}") from exc

    # Rimuove i file temporanei dei grafici
    for path in (grafico_path, grafico_avanzato_path, grafico_lux_db_path):
        try:
            os.remove(path)
        except OSError:
            pass

    return output_path
