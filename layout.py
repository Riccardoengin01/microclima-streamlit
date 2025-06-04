# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import streamlit as st

# Modifica CSS per sidebar più larga e non centrata
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            width: 60%; /* Puoi regolare la percentuale per maggiore larghezza */
            min-width: 1100px; /* Imposta una larghezza minima */
        }
        .block-container {
            padding-left: 5%; /* Riduce il padding per allineare al resto */
            padding-right: 5%;
        }
    </style>
""", unsafe_allow_html=True)

def setup_layout(parametri_definizioni):
    st.title("Analisi del Microclima Ufficio")
    st.subheader("(UNI EN ISO 7730 e D.Lgs. 81/08)")

    st.sidebar.header("Inserisci i parametri ambientali")

    temp_aria = st.sidebar.number_input(
        "Temperatura aria (°C):", min_value=10.0, max_value=40.0, value=22.0, step=0.1
    )
    st.sidebar.caption(parametri_definizioni["temp_aria"])

    temp_radiante = st.sidebar.number_input(
        "Temperatura radiante media (°C):", min_value=10.0, max_value=40.0, value=22.0, step=0.1
    )
    st.sidebar.caption(parametri_definizioni["temp_radiante"])

    vel_aria = st.sidebar.number_input(
        "Velocità aria (m/s):", min_value=0.0, max_value=1.0, value=0.1, step=0.1
    )
    st.sidebar.caption(parametri_definizioni["vel_aria"])

    umidita = st.sidebar.number_input(
        "Umidità relativa (%):", min_value=30.0, max_value=70.0, value=50.0, step=1.0
    )
    st.sidebar.caption(parametri_definizioni["umidita"])

    metabolismo = st.sidebar.number_input(
        "Metabolismo (Met):", min_value=0.8, max_value=4.0, value=1.2, step=0.1
    )
    st.sidebar.caption(parametri_definizioni["metabolismo"])

    isolamento = st.sidebar.number_input(
        "Isolamento termico (Clo):", min_value=0.0, max_value=2.0, value=0.5, step=0.1
    )
    st.sidebar.caption(parametri_definizioni["isolamento"])

    submit = st.sidebar.button("Calcola")

    return {
        "temp_aria": temp_aria, "temp_radiante": temp_radiante, "vel_aria": vel_aria,
        "umidita": umidita, "metabolismo": metabolismo, "isolamento": isolamento,
        "submit": submit
    }
