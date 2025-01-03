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
    Calcola PMV e PPD basati sul modello VBA adattato in Python.
    """
    import math

    FNPS = math.exp(16.6536 - 4030.183 / (temp_aria + 235))
    PA = umidita * 10 * FNPS
    ICL = 0.155 * isolamento
    M = metabolismo * 58.15

    # Calcolo FCL
    if ICL < 0.078:
        FCL = 1 + 1.29 * ICL
    else:
        FCL = 1.05 + 0.645 * ICL

    # Parametri intermedi
    HCF = 12.1 * vel_aria ** 0.5
    TAA = temp_aria + 273
    TRA = temp_radiante + 273
    TCLA = TAA + (35.5 - temp_aria) / (3.5 * (6.45 * ICL + 0.1))

    # Iterazioni per calcolo TCL
    P1 = ICL * FCL
    P2 = P1 * 3.96
    P3 = P1 * 100
    P4 = P1 * TAA
    P5 = 308.7 - 0.028 * M + P2 * (TRA / 100) ** 4

    XN = TCLA / 100
    XF = TCLA / 50
    EPS = 0.0015
    while abs(XN - XF) > EPS:
        XF = (XF + XN) / 2
        HCN = 2.38 * abs(100 * XF - TAA) ** 0.25
        HC = max(HCF, HCN)
        XN = (P5 + P4 * HC - P2 * (XF ** 4)) / (100 + P3 * HC)

    TCL = 100 * XN - 273

    # Calcoli termici
    HL1 = 3.05 * 0.001 * (5733 - 6.99 * M - PA)
    HL2 = 0.42 * (M - 58.15) if M > 58.15 else 0
    HL3 = 1.7 * 0.00001 * M * (5867 - PA)
    HL4 = 0.0014 * M * (34 - temp_aria)
    HL5 = 3.96 * FCL * (XN ** 4 - (TRA / 100) ** 4)
    HL6 = FCL * HC * (TCL - temp_aria)

    # PMV e PPD
    TS = 0.303 * math.exp(-0.036 * M) + 0.028
    PMV = TS * (M - HL1 - HL2 - HL3 - HL4 - HL5 - HL6)
    PPD = 100 - 95 * math.exp(-0.03353 * PMV ** 4 - 0.2179 * PMV ** 2)

    return {"pmv": PMV, "ppd": PPD}

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

