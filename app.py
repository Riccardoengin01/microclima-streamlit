import streamlit as st

# CSS per personalizzare lo stile della sidebar
st.markdown(
    """
    <style>
    /* Allarga la sidebar */
    [data-testid="stSidebar"] {
        min-width: 400px; /* Modifica la larghezza */
        max-width: 400px;
        overflow-y: auto; /* Aggiungi scorrimento verticale */
    }

    /* Modifica lo stile generale */
    .css-1d391kg {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }

    /* Stile per i parametri */
    .parameter-section {
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Titolo
st.title("Analisi del Microclima Ufficio")
st.subheader("(UNI EN ISO 7730 e D.Lgs. 81/08)")

# Parametri nella sidebar con sezioni
with st.sidebar:
    st.header("Parametri Ambientali")

    st.markdown("<div class='parameter-section'>", unsafe_allow_html=True)
    temp_aria = st.number_input(
        "Temperatura aria (°C):", min_value=10.0, max_value=40.0, value=22.0, step=0.1
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='parameter-section'>", unsafe_allow_html=True)
    temp_radiante = st.number_input(
        "Temperatura radiante media (°C):", min_value=10.0, max_value=40.0, value=22.0, step=0.1
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='parameter-section'>", unsafe_allow_html=True)
    vel_aria = st.number_input(
        "Velocità aria (m/s):", min_value=0.0, max_value=1.0, value=0.1, step=0.1
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='parameter-section'>", unsafe_allow_html=True)
    umidita = st.number_input(
        "Umidità relativa (%):", min_value=30.0, max_value=70.0, value=50.0, step=1.0
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='parameter-section'>", unsafe_allow_html=True)
    metabolismo = st.number_input(
        "Metabolismo (Met):", min_value=0.8, max_value=4.0, value=1.2, step=0.1
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='parameter-section'>", unsafe_allow_html=True)
    isolamento = st.number_input(
        "Isolamento termico (Clo):", min_value=0.0, max_value=2.0, value=0.5, step=0.1
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Bottone per calcolare
if st.sidebar.button("Calcola"):
    st.write(f"Temperatura aria: {temp_aria} °C")
    st.write(f"Temperatura radiante: {temp_radiante} °C")
    st.write(f"Velocità aria: {vel_aria} m/s")
    st.write(f"Umidità relativa: {umidita} %")
    st.write(f"Metabolismo: {metabolismo} Met")
    st.write(f"Isolamento termico: {isolamento} Clo")
