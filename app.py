# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import streamlit as st
from pythermalcomfort.models import pmv_ppd_iso
from layout import setup_layout  # Importa il modulo layout
from spiegazioni_indici import spiegazioni_indici
from parametri_definizioni import parametri_definizioni
from pdf_generator import genera_report_pdf
from grafici import genera_grafico_pmv_ppd


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
inputs = setup_layout(parametri_definizioni)

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

    st.subheader("Risultati")
    st.write(f"**Indice PMV:** {pmv:.2f}")
    st.text(spiegazioni_indici["pmv"])
    st.write(f"**Indice PPD:** {ppd:.2f}%")
    st.text(spiegazioni_indici["ppd"])

    grafico = genera_grafico_pmv_ppd(pmv, ppd)
    st.image(grafico, caption="Relazione tra PMV e PPD")

    report_pdf = genera_report_pdf(
        inputs["temp_aria"],
        inputs["temp_radiante"],
        inputs["vel_aria"],
        inputs["umidita"],
        inputs["metabolismo"],
        inputs["isolamento"],
        pmv,
        ppd,
        inputs["sede"],
        inputs["descrizione_locale"],
    )
    with open(report_pdf, "rb") as file:
        st.download_button(
            "Scarica Report PDF",
            file.read(),
            file_name="report_microclima.pdf",
            mime="application/pdf",
        )
