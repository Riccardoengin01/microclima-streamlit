import streamlit as st

def setup_layout(parametri_definizioni):
    # Applica stile personalizzato per la sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                min-width: 300px;
                max-width: 350px;
            }
            .block-container {
                padding: 1rem 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Colonne per dividere gli input
    col1, col2 = st.columns(2)

    # Input nella colonna di sinistra
    with col1:
        st.header("Parametri di Input - Parte 1")
        temp_aria = st.number_input(
            "Temperatura aria (°C):",
            min_value=10.0, max_value=40.0, value=22.0, step=0.1,
            help=parametri_definizioni["temp_aria"]
        )
        temp_radiante = st.number_input(
            "Temperatura radiante media (°C):",
            min_value=10.0, max_value=40.0, value=22.0, step=0.1,
            help=parametri_definizioni["temp_radiante"]
        )
        vel_aria = st.number_input(
            "Velocità aria (m/s):",
            min_value=0.0, max_value=1.0, value=0.1, step=0.1,
            help=parametri_definizioni["vel_aria"]
        )

    # Input nella colonna di destra
    with col2:
        st.header("Parametri di Input - Parte 2")
        umidita = st.number_input(
            "Umidità relativa (%):",
            min_value=30.0, max_value=70.0, value=50.0, step=1.0,
            help=parametri_definizioni["umidita"]
        )
        metabolismo = st.number_input(
            "Metabolismo (Met):",
            min_value=0.8, max_value=4.0, value=1.2, step=0.1,
            help=parametri_definizioni["metabolismo"]
        )
        isolamento = st.number_input(
            "Isolamento termico (Clo):",
            min_value=0.0, max_value=2.0, value=0.5, step=0.1,
            help=parametri_definizioni["isolamento"]
        )

    # Bottone per calcolare
    submit = st.button("Calcola")

    # Restituisce i parametri raccolti
    return {
        "temp_aria": temp_aria,
        "temp_radiante": temp_radiante,
        "vel_aria": vel_aria,
        "umidita": umidita,
        "metabolismo": metabolismo,
        "isolamento": isolamento,
        "submit": submit
    }
