import streamlit as st

# Forza la larghezza della sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 400px;
        overflow-x: hidden;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Analisi del Microclima Ufficio")
st.subheader("(UNI EN ISO 7730 e D.Lgs. 81/08)")

st.sidebar.header("Inserisci i parametri ambientali")

temp_aria = st.sidebar.number_input(
    "Temperatura aria (°C):", min_value=10.0, max_value=40.0, value=22.0, step=0.1
)
temp_radiante = st.sidebar.number_input(
    "Temperatura radiante media (°C):", min_value=10.0, max_value=40.0, value=22.0, step=0.1
)
vel_aria = st.sidebar.number_input(
    "Velocità aria (m/s):", min_value=0.0, max_value=1.0, value=0.1, step=0.1
)
umidita = st.sidebar.number_input(
    "Umidità relativa (%):", min_value=30.0, max_value=70.0, value=50.0, step=1.0
)
metabolismo = st.sidebar.number_input(
    "Metabolismo (Met):", min_value=0.8, max_value=4.0, value=1.2, step=0.1
)
isolamento = st.sidebar.number_input(
    "Isolamento termico (Clo):", min_value=0.0, max_value=2.0, value=0.5, step=0.1
)

if st.sidebar.button("Calcola"):
    st.write("Calcolo eseguito!")
