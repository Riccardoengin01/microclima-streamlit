# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.
"""Avvia l'interfaccia Streamlit richiamando ``setup_layout``."""

import layout


def main() -> None:
    """Esegue ``setup_layout`` dal modulo ``layout``."""
    layout.setup_layout()


if __name__ == "__main__":
    main()
