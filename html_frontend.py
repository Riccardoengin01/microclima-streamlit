# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

"""Semplice frontend HTML basato su Flask."""

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Rende la pagina principale e gestisce il form."""
    if request.method == "POST":
        return render_template("index.html", message="Dati ricevuti")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
