# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import streamlit_main


def test_main_chiama_setup(monkeypatch):
    chiamato = {}

    def finta_setup():
        chiamato["ok"] = True

    monkeypatch.setattr(streamlit_main.layout, "setup_layout", finta_setup)
    streamlit_main.main()
    assert chiamato.get("ok")
