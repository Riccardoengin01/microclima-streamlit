# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

"""Semplice frontend HTML basato su Flask."""

from flask import Flask, render_template, request
from spiegazioni_indici import spiegazioni_indici
from parametri_definizioni import parametri_definizioni

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Rende la pagina principale e gestisce il form."""
    illuminazione = None
    impatto_acustico = None
    if request.method == "POST":
        try:
            illuminazione = float(request.form.get("illuminazione", 0))
            impatto_acustico = float(request.form.get("impatto_acustico", 0))
            message = "Dati ricevuti"
        except ValueError:
            message = "Valori non validi"
        return render_template(
            "index.html",
            message=message,
            illuminazione=illuminazione,
            impatto_acustico=impatto_acustico,
            spiegazioni=spiegazioni_indici,
            definizioni=parametri_definizioni,
        )
    return render_template(
        "index.html",
        spiegazioni=spiegazioni_indici,
        definizioni=parametri_definizioni,
    )


if __name__ == "__main__":
    app.run(debug=True)
