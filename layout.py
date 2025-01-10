import streamlit as st

def setup_layout(parametri_definizioni):
    st.title("Analisi del Microclima Ufficio")
    st.subheader("(UNI EN ISO 7730 e D.Lgs. 81/08)")

    st.sidebar.header("Inserisci i parametri ambientali")

    col1, col2 = st.columns(2)  # Due colonne per i parametri

    with col1:
        temp_aria = st.number_input(
            "Temperatura aria (°C):", min_value=10.0, max_value=40.0, value=22.0, step=0.1
        )
        st.caption(parametri_definizioni["temp_aria"])

        temp_radiante = st.number_input(
            "Temperatura radiante media (°C):", min_value=10.0, max_value=40.0, value=22.0, step=0.1
        )
        st.caption(parametri_definizioni["temp_radiante"])

        vel_aria = st.number_input(
            "Velocità aria (m/s):", min_value=0.0, max_value=1.0, value=0.1, step=0.1
        )
        st.caption(parametri_definizioni["vel_aria"])

    with col2:
        umidita = st.number_input(
            "Umidità relativa (%):", min_value=30.0, max_value=70.0, value=50.0, step=1.0
        )
        st.caption(parametri_definizioni["umidita"])

        metabolismo = st.number_input(
            "Metabolismo (Met):", min_value=0.8, max_value=4.0, value=1.2, step=0.1
        )
        st.caption(parametri_definizioni["metabolismo"])

        isolamento = st.number_input(
            "Isolamento termico (Clo):", min_value=0.0, max_value=2.0, value=0.5, step=0.1
        )
        st.caption(parametri_definizioni["isolamento"])

    submit = st.button("Calcola")

    return {
        "temp_aria": temp_aria, "temp_radiante": temp_radiante, "vel_aria": vel_aria,
        "umidita": umidita, "metabolismo": metabolismo, "isolamento": isolamento,
        "submit": submit
    }
