# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import streamlit as st
from pythermalcomfort.models import pmv_ppd_iso
from layout import setup_layout
from spiegazioni_indici import spiegazioni_indici, spiegazioni_indici_en
from pdf_generator import genera_report_pdf
from grafici import (
    genera_grafico_pmv_ppd,
    genera_grafico_pmv_ppd_avanzato,
    genera_grafico_lux_db,
)
import os
from traduzioni import LABELS


# Calcolo PMV e PPD tramite pythermalcomfort (ISO 7730)
def calcola_microclima(
    temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento
):
    """Restituisce PMV e PPD calcolati secondo la ISO 7730."""
    result = pmv_ppd_iso(
        tdb=temp_aria,
        tr=temp_radiante,
        vr=vel_aria,
        rh=umidita,
        met=metabolismo,
        clo=isolamento,
        wme=0,
        round_output=False,
    )
    return {"pmv": result.pmv, "ppd": result.ppd}


# Layout e parametri
inputs = setup_layout()

# Calcolo e risultati
if inputs["submit"]:
    risultati = calcola_microclima(
        inputs["temp_aria"],
        inputs["temp_radiante"],
        inputs["vel_aria"],
        inputs["umidita"],
        inputs["metabolismo"],
        inputs["isolamento"],
    )
    pmv, ppd = risultati["pmv"], risultati["ppd"]

    testi = LABELS[inputs["lingua"]]
    spiegazioni = (
        spiegazioni_indici if inputs["lingua"] == "it" else spiegazioni_indici_en
    )
    st.subheader(testi["results"])
    st.write(f"**{testi['pmv']}** {pmv:.2f}")
    st.text(spiegazioni["pmv"])
    st.write(f"**{testi['ppd']}** {ppd:.2f}%")
    st.text(spiegazioni["ppd"])

    grafico_base = genera_grafico_pmv_ppd(pmv, ppd)
    grafico_avanzato = genera_grafico_pmv_ppd_avanzato(
        pmv, ppd, inputs["temp_aria"], inputs["umidita"]
    )
    grafico_lux_db = genera_grafico_lux_db(
        inputs["illuminazione"], inputs["impatto_acustico"]
    )

    col1, col2, col3 = st.columns(3)
    col1.image(grafico_base, caption="Relazione tra PMV e PPD")
    col2.image(grafico_avanzato, caption="Grafico avanzato PMV-PPD")
    col3.image(grafico_lux_db, caption="Illuminazione e Rumore")

    for path in (grafico_base, grafico_avanzato, grafico_lux_db):
        try:
            os.remove(path)
        except OSError:
            pass

    report_name = f"report_{inputs['sede'].replace(' ', '_')}_{inputs['descrizione_locale'].replace(' ', '_')}.pdf"
    report_pdf = genera_report_pdf(
        inputs["temp_aria"],
        inputs["temp_radiante"],
        inputs["vel_aria"],
        inputs["umidita"],
        inputs["illuminazione"],
        inputs["impatto_acustico"],
        inputs["metabolismo"],
        inputs["isolamento"],
        pmv,
        ppd,
        inputs["sede"],
        inputs["descrizione_locale"],
        output_path=report_name,
        data=inputs["data"],
        lingua=inputs["lingua"],
    )
    with open(report_pdf, "rb") as file:
        st.download_button(
            LABELS[inputs["lingua"]]["download"],
            file.read(),
            file_name=report_name,
            mime="application/pdf",
        )
