import os
os.system('pip install pythermalcomfort matplotlib fpdf')

import streamlit as st
from fpdf import FPDF
import matplotlib.pyplot as plt
import io
import math

# Funzione per calcolare PMV e PPD basati sulle formule della norma UNI EN ISO 7730
def calcola_microclima(temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento):
    FNPS = math.exp(16.6536 - 4030.183 / (temp_aria + 235))
    PA = umidita * 10 * FNPS
    ICL = 0.155 * isolamento
    M = metabolismo * 58.15

    if ICL < 0.078:
        FCL = 1 + 1.29 * ICL
    else:
        FCL = 1.05 + 0.645 * ICL

    HCF = 12.1 * vel_aria ** 0.5
    TAA = temp_aria + 273
    TRA = temp_radiante + 273
    TCLA = TAA + (35.5 - temp_aria) / (3.5 * (6.45 * ICL + 0.1))

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

    HL1 = 3.05 * 0.001 * (5733 - 6.99 * M - PA)
    HL2 = 0.42 * (M - 58.15) if M > 58.15 else 0
    HL3 = 1.7 * 0.00001 * M * (5867 - PA)
    HL4 = 0.0014 * M * (34 - temp_aria)
    HL5 = 3.96 * FCL * (XN ** 4 - (TRA / 100) ** 4)
    HL6 = FCL * HC * (TCL - temp_aria)

    TS = 0.303 * math.exp(-0.036 * M) + 0.028
    PMV = TS * (M - HL1 - HL2 - HL3 - HL4 - HL5 - HL6)
    PPD = 100 - 95 * math.exp(-0.03353 * PMV ** 4 - 0.2179 * PMV ** 2)

    return {"pmv": PMV, "ppd": PPD}

# Funzione per generare il grafico PMV-PPD
def genera_grafico_pmv_ppd(pmv, ppd):
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

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf

from pdf_generator import genera_report_pdf

# Interfaccia utente Streamlit
st.title("Analisi del Microclima Ufficio (UNI EN ISO 7730 e D.Lgs. 81/08)")
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

    grafico_buffer = genera_grafico_pmv_ppd(pmv, ppd)
    st.image(grafico_buffer, caption="Relazione tra PMV e PPD")

    # Download del report
    report_pdf = genera_report_pdf(temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento, pmv, ppd)
    with open(report_pdf, "rb") as file:
        st.download_button(
            label="Scarica Report PDF",
            data=file,
            file_name="report_microclima.pdf",
            mime="application/pdf"
        )

