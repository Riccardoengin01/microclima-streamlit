# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import streamlit as st
from traduzioni import LABELS
from parametri_definizioni import (
    parametri_definizioni,
    parametri_definizioni_en,
    soglie_parametri,
)

# Modifica CSS per sidebar più larga e non centrata
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)


def setup_layout():
    """Imposta il layout della pagina e restituisce i valori inseriti.

    Ritorna:
        dict: valori forniti dall'utente e stato del pulsante.
    """
    lingua_sel = st.sidebar.selectbox("Lingua", ["Italiano", "English"])
    lang_code = "it" if lingua_sel == "Italiano" else "en"
    testi = LABELS[lang_code]
    definizioni = (
        parametri_definizioni if lang_code == "it" else parametri_definizioni_en
    )

    st.title(testi["title"])
    st.subheader(testi["subheader"])

    st.sidebar.header(testi["sidebar_header"])

    sede = st.sidebar.text_input(testi["location"])
    descrizione_locale = st.sidebar.text_input(testi["description"])
    data = st.sidebar.date_input(testi["date"])

    temp_aria = st.sidebar.number_input(
        testi["air_temp"], min_value=10.0, max_value=40.0, value=22.0, step=0.1
    )
    st.sidebar.caption(definizioni["temp_aria"])

    temp_radiante = st.sidebar.number_input(
        testi["rad_temp"],
        min_value=10.0,
        max_value=40.0,
        value=22.0,
        step=0.1,
    )
    st.sidebar.caption(definizioni["temp_radiante"])

    vel_aria = st.sidebar.number_input(
        testi["air_speed"], min_value=0.0, max_value=1.0, value=0.1, step=0.1
    )
    st.sidebar.caption(definizioni["vel_aria"])

    umidita = st.sidebar.number_input(
        testi["humidity"], min_value=30.0, max_value=70.0, value=50.0, step=1.0
    )
    st.sidebar.caption(definizioni["umidita"])

    metabolismo = st.sidebar.number_input(
        testi["metabolism"], min_value=0.8, max_value=4.0, value=1.2, step=0.1
    )
    st.sidebar.caption(definizioni["metabolismo"])

    isolamento = st.sidebar.number_input(
        testi["insulation"], min_value=0.0, max_value=2.0, value=0.5, step=0.1
    )
    st.sidebar.caption(definizioni["isolamento"])

    illuminazione = st.sidebar.number_input(
        testi["lighting"], min_value=0.0, max_value=2000.0, value=500.0, step=1.0
    )
    st.sidebar.caption(definizioni["illuminazione"])
    lux_min, lux_max = soglie_parametri["illuminazione"]
    if lang_code == "it":
        st.sidebar.caption(f"Soglia consigliata {lux_min}-{lux_max} lux")
    else:
        st.sidebar.caption(f"Recommended range {lux_min}-{lux_max} lux")

    impatto_acustico = st.sidebar.number_input(
        testi["noise"], min_value=30.0, max_value=120.0, value=50.0, step=1.0
    )
    st.sidebar.caption(definizioni["impatto_acustico"])
    db_min, db_max = soglie_parametri["impatto_acustico"]
    if lang_code == "it":
        st.sidebar.caption(f"Soglia consigliata {db_min}-{db_max} dB")
    else:
        st.sidebar.caption(f"Recommended range {db_min}-{db_max} dB")

    commento_responsabile = st.sidebar.text_area(testi["manager_comments"])
    firma_responsabile = st.sidebar.text_input(testi["manager_signature"])

    submit = st.sidebar.button(testi["submit"])

    return {
        "sede": sede,
        "descrizione_locale": descrizione_locale,
        "temp_aria": temp_aria,
        "temp_radiante": temp_radiante,
        "vel_aria": vel_aria,
        "umidita": umidita,
        "metabolismo": metabolismo,
        "isolamento": isolamento,
        "illuminazione": illuminazione,
        "impatto_acustico": impatto_acustico,
        "commento_responsabile": commento_responsabile,
        "firma_responsabile": firma_responsabile,
        "data": data,
        "submit": submit,
        "lingua": lang_code,
    }
