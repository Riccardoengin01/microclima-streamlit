%%writefile app.py
import streamlit as st
from pythermalcomfort.models import pmv_ppd

# Funzione per calcolare PMV e PPD
def calcola_microclima(temp_aria, umidita, vel_aria, metabolismo, isolamento):
    """
    Calcola PMV e PPD basati sui parametri forniti.
    """
    risultato = pmv_ppd(
        tdb=temp_aria,    # Temperatura dell'aria secca (°C)
        tr=temp_aria,     # Temperatura radiante media (assunta uguale a tdb)
        vr=vel_aria,      # Velocità relativa dell'aria (m/s)
        rh=umidita,       # Umidità relativa (%)
        met=metabolismo,  # Metabolismo (Met)
        clo=isolamento    # Isolamento termico (Clo)
    )
    return risultato

# Interfaccia utente con Streamlit
st.title("Analisi del Microclima Ufficio")
st.markdown("""
Questa applicazione ti permette di calcolare l'indice PMV (Predicted Mean Vote) e PPD 
(Predicted Percentage of Dissatisfied) per valutare il comfort termico di un ambiente.
""")

# Input dell'utente
st.sidebar.header("Inserisci i parametri ambientali")
temp_aria = st.sidebar.number_input("Temperatura aria (°C):", min_value=0.0, max_value=50.0, value=22.0, step=0.1)
umidita = st.sidebar.number_input("Umidità relativa (%):", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
vel_aria = st.sidebar.number_input("Velocità aria (m/s):", min_value=0.0, max_value=5.0, value=0.1, step=0.1)
metabolismo = st.sidebar.number_input("Metabolismo (Met):", min_value=0.0, max_value=5.0, value=1.2, step=0.1)
isolamento = st.sidebar.number_input("Isolamento termico (Clo):", min_value=0.0, max_value=2.0, value=0.5, step=0.1)

# Bottone per calcolare i risultati
if st.button("Calcola"):
    risultati = calcola_microclima(temp_aria, umidita, vel_aria, metabolismo, isolamento)
    pmv = risultati['pmv']
    ppd = risultati['ppd']

    # Mostra i risultati
    st.subheader("Risultati")
    st.write(f"**Indice PMV:** {pmv:.2f}")
    st.write(f"**Indice PPD:** {ppd:.2f}%")

    # Interpretazione dei risultati
    if pmv < -0.5:
        st.warning("Comfort termico troppo freddo. Consigli: aumentare la temperatura.")
    elif pmv > 0.5:
        st.warning("Comfort termico troppo caldo. Consigli: abbassare la temperatura.")
    else:
        st.success("Comfort termico accettabile.")

    if ppd > 10:
        st.error(f"PPD alto ({ppd:.2f}%): molte persone potrebbero non essere soddisfatte.")
    else:
        st.success("La maggior parte delle persone è soddisfatta del comfort termico.")
