import os
os.system('pip install pythermalcomfort matplotlib fpdf')

import streamlit as st
from pythermalcomfort.models import pmv_ppd
from pythermalcomfort.utilities import clo_dynamic, v_relative
from fpdf import FPDF
import matplotlib.pyplot as plt

# Funzione per calcolare PMV e PPD
def calcola_microclima(temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento):
    """
    Calcola PMV e PPD secondo UNI EN ISO 7730 e converte i valori per il D.Lgs. 81/08.
    """
    # Convertiamo velocità relativa e isolamento dinamico
    vel_relativa = v_relative(v=vel_aria, met=metabolismo)
    isolamento_dinamico = clo_dynamic(clo=isolamento, met=metabolismo)

    # Calcolo del PMV e PPD
    risultato = pmv_ppd(
        tdb=temp_aria,           # Temperatura dell'aria (°C)
        tr=temp_radiante,        # Temperatura radiante media (°C)
        vr=vel_relativa,         # Velocità relativa dell'aria (m/s)
        rh=umidita,              # Umidità relativa (%)
        met=metabolismo,         # Metabolismo (Met)
        clo=isolamento_dinamico, # Isolamento termico dinamico (Clo)
        standard="ISO"           # Specifica l'uso della norma ISO
    )
    return risultato

# Funzione per generare il report PDF
def genera_pdf(temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento, pmv, ppd):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Analisi del Microclima Ufficio", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Parametri inseriti:", ln=True)
    pdf.cell(200, 10, txt=f"Temperatura aria: {temp_aria} °C", ln=True)
    pdf.cell(200, 10, txt=f"Temperatura radiante media: {temp_radiante} °C", ln=True)
    pdf.cell(200, 10, txt=f"Velocità aria: {vel_aria} m/s", ln=True)
    pdf.cell(200, 10, txt=f"Umidità relativa: {umidita} %", ln=True)
    pdf.cell(200, 10, txt=f"Metabolismo: {metabolismo} Met", ln=True)
    pdf.cell(200, 10, txt=f"Isolamento termico: {isolamento} Clo", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Risultati:", ln=True)
    pdf.cell(200, 10, txt=f"Indice PMV: {pmv:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Indice PPD: {ppd:.2f} %", ln=True)

    pdf.cell(200, 10, txt="Conformità normativa:", ln=True)
    if -0.5 <= pmv <= 0.5 and ppd <= 10:
        pdf.cell(200, 10, txt="I valori rispettano la normativa UNI EN ISO 7730 e il D.Lgs. 81/08.", ln=True)
    else:
        pdf.cell(200, 10, txt="I valori NON rispettano le condizioni di comfort richieste.", ln=True)

    pdf.output("report_microclima.pdf")

# Interfaccia utente con Streamlit
st.title("Analisi del Microclima Ufficio (Conformità UNI EN ISO 7730 e D.Lgs. 81/08)")
st.sidebar.header("Inserisci i parametri ambientali")
temp_aria = st.sidebar.number_input("Temperatura aria (°C):", min_value=-10.0, max_value=50.0, value=22.0, step=0.1)
temp_radiante = st.sidebar.number_input("Temperatura radiante media (°C):", min_value=-10.0, max_value=50.0, value=22.0, step=0.1)
vel_aria = st.sidebar.number_input("Velocità aria (m/s):", min_value=0.0, max_value=5.0, value=0.1, step=0.1)
umidita = st.sidebar.number_input("Umidità relativa (%):", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
metabolismo = st.sidebar.number_input("Metabolismo (Met):", min_value=0.0, max_value=5.0, value=1.2, step=0.1)
isolamento = st.sidebar.number_input("Isolamento termico (Clo):", min_value=0.0, max_value=2.0, value=0.5, step=0.1)

# Bottone per calcolare i risultati
if st.button("Calcola"):
    risultati = calcola_microclima(temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento)
    pmv = risultati['pmv']
    ppd = risultati['ppd']

    st.subheader("Risultati")
    st.write(f"**Indice PMV:** {pmv:.2f}")
    st.write(f"**Indice PPD:** {ppd:.2f}%")

    # Conformità normativa
    if -0.5 <= pmv <= 0.5 and ppd <= 10:
        st.success("I valori rispettano la normativa UNI EN ISO 7730 e il D.Lgs. 81/08.")
    else:
        st.error("I valori NON rispettano le condizioni di comfort richieste.")

    # Generazione del report PDF
    if st.button("Scarica report PDF"):
        genera_pdf(temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento, pmv, ppd)
        st.success("Report PDF generato! Controlla la cartella di output.")

