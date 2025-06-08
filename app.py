# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

"""Applicazione Flask per il calcolo di PMV e PPD."""

from flask import Flask, render_template, request
from pythermalcomfort.models import pmv_ppd_iso
import os

app = Flask(__name__)


def calcola_microclima(
    temp_aria, temp_radiante, vel_aria, umidita, metabolismo, isolamento
):
    """Restituisce PMV e PPD calcolati secondo la ISO 7730."""
    result = pmv_ppd_iso(
        tdb=temp_aria,
        tr=temp_radiante,
        vr=vel_aria,
        rh=umidita,
        met=metabolismo,
        clo=isolamento,
        wme=0,
        round_output=False,
    )
    return {"pmv": result.pmv, "ppd": result.ppd}


def calcola_pmv_ppd(temp_aria, temp_radiante, vel_aria, umidita, clo, met):
    """Wrapper che richiama :func:`calcola_microclima`."""
    return calcola_microclima(temp_aria, temp_radiante, vel_aria, umidita, met, clo)


@app.route("/", methods=["GET", "POST"])
def index():
    """Gestisce il form e mostra i risultati del calcolo."""
    result = None
    if request.method == "POST":
        try:
            temp_aria = float(request.form.get("temp_aria", 0))
            temp_radiante = float(request.form.get("temp_radiante", temp_aria))
            umidita = float(request.form.get("umidita", 0))
            vel_aria = float(request.form.get("vel_aria", 0))
            clo = float(request.form.get("clo", 0))
            met = float(request.form.get("met", 0))
            result = calcola_pmv_ppd(
                temp_aria, temp_radiante, vel_aria, umidita, clo, met
            )
        except ValueError:
            result = None
    return render_template("index.html", result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # 10000 è la porta che userai su Render
    app.run(host="0.0.0.0", port=port)
