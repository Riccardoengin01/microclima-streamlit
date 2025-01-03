import os
os.system('pip install fpdf matplotlib')

import os
os.system('pip install pythermalcomfort fpdf matplotlib')

import streamlit as st
from pythermalcomfort.models import pmv_ppd
from fpdf import FPDF
import matplotlib.pyplot as plt

# Funzione per calcolare PMV e PPD
def calcola_microclima(temp_aria, umidita, vel_aria, metabolismo, isolamento):
    """
    Calcola PMV e PPD basati sui parametri forniti.
    """
    try:
        risultato = pmv_ppd(
            tdb=temp_aria,    # Temperatura dell'aria secca (°C)
            tr=temp_aria,     # Temperatura radiante media (assunta uguale a tdb)
            vr=vel_aria,      # Velocità relativa dell'aria (m/s)
            rh=umidita,       # Umidità relativa (%)
            met=metabolismo,  # Metabolismo (Met)
            clo=isolamento    # Isolamento termico (Clo)
        )
        return risultato
    except Exception as e:
        return {"pmv": None, "ppd": None, "error": str(e)}

# Funzione per generare PDF
def genera_pdf(temp_aria, umidita, vel_aria, metabolismo, isolamento, pmv, ppd):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Analisi del Microclima Ufficio", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Parametri inseriti:", ln=True)
    pdf.cell(200, 10, txt=f"- Temperatura aria: {temp_aria} °C", ln=True)
    pdf.cell(200, 10, txt=f"- Umidità relativa: {umidita} %", ln=True)
    pdf.cell(200, 10, txt=f"- Velocità aria: {vel_aria} m/s", ln=True)
    pdf.cell(200, 10, txt=f"- Metabolismo: {metabolismo} Met", ln=True)
    pdf.cell(200, 10, txt=f"- Isolamento termico: {isolamento} Clo", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Risultati:", ln=True)
    pdf.cell(200, 10, txt=f"- Indice PMV: {pmv:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"- Indice PPD: {ppd:.2f}%", ln=True)
    pdf.ln(10)

    if pmv < -0.5:
        pdf.cell(200, 10, txt="Comfort termico troppo freddo.", ln=True)
    elif pmv > 0.5:
        pdf.cell(200, 10, txt="Comfort termico troppo caldo.", ln=True)
    else:
        pdf.cell(200, 10, txt="Comfort termico accettabile.", ln=True)

    if ppd > 10:
        pdf.cell(200, 10, txt=f"Molte persone ({ppd:.2f}%) potrebbero non essere soddisfatte.", ln=True)
    else:
        pdf.cell(200, 10, txt="La maggior parte delle persone è soddisfatta del comfort termico.", ln=True)

    pdf.output("report_microclima.pdf")
    return "report_microclima.pdf"

# Funzione per generare il grafico
def genera_grafico(pmv):
    fig, ax = plt.subplots()
    categorie = ['Troppo freddo', 'Accettabile', 'Troppo caldo']
    valori = [1 if pmv < -0.5 else 0, 1 if -0.5 <= pmv <= 0.5 else 0, 1 if pmv > 0.5 else 0]

    ax.bar(categorie, valori, color=['blue', 'green', 'red'])
    ax.set_ylabel("Comfort termico")
    ax.set_title("Distribuzione comfort termico")
    st.pyplot(fig)

# Interfaccia utente con Streamlit
st.title("Analisi del Microclima Ufficio")

# Multilingua
lingua = st.sidebar.selectbox("Seleziona la lingua / Select Language", ["Italiano", "English"])
if lingua == "Italiano":
    st.sidebar.header("Inserisci i parametri ambientali")
else:
    st.sidebar.header("Enter environmental parameters")

temp_aria = st.sidebar.number_input("Temperatura aria (°C):" if lingua == "Italiano" else "Air temperature (°C):", min_value=0.0, max_value=50.0, value=22.0, step=0.1)
umidita = st.sidebar.number_input("Umidità relativa (%):" if lingua == "Italiano" else "Relative humidity (%):", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
vel_aria = st.sidebar.number_input("Velocità aria (m/s):" if lingua == "Italiano" else "Air speed (m/s):", min_value=0.0, max_value=5.0, value=0.1, step=0.1)
metabolismo = st.sidebar.number_input("Metabolismo (Met):" if lingua == "Italiano" else "Metabolism (Met):", min_value=0.0, max_value=5.0, value=1.2, step=0.1)
isolamento = st.sidebar.number_input("Isolamento termico (Clo):" if lingua == "Italiano" else "Thermal insulation (Clo):", min_value=0.0, max_value=2.0, value=0.5, step=0.1)

# Bottone per calcolare
if st.button("Calcola" if lingua == "Italiano" else "Calculate"):
    risultati = calcola_microclima(temp_aria, umidita, vel_aria, metabolismo, isolamento)

    if risultati["pmv"] is not None and risultati["ppd"] is not None:
        pmv = risultati["pmv"]
        ppd = risultati["ppd"]

        st.subheader("Risultati" if lingua == "Italiano" else "Results")
        st.write(f"**Indice PMV:** {pmv:.2f}")
        st.write(f"**Indice PPD:** {ppd:.2f}%")

        genera_grafico(pmv)

        pdf_path = genera_pdf(temp_aria, umidita, vel_aria, metabolismo, isolamento, pmv, ppd)
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Scarica il report in PDF" if lingua == "Italiano" else "Download PDF Report",
                data=file,
                file_name="report_microclima.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Errore durante il calcolo." if lingua == "Italiano" else "Error during calculation.")
