# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

"""Applicazione Flask per il calcolo di PMV e PPD."""

from flask import Flask, render_template, request, send_file, after_this_request, abort
from pythermalcomfort.models import pmv_ppd_iso
import os
import tempfile

from spiegazioni_indici import spiegazioni_indici
from parametri_definizioni import parametri_definizioni
from pdf_generator import genera_report_pdf

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
    temp_aria = None
    temp_radiante = None
    umidita = None
    vel_aria = None
    clo = None
    met = None
    illuminazione = None
    impatto_acustico = None
    if request.method == "POST":
        try:
            temp_aria = float(request.form.get("temp_aria", 0))
            temp_radiante = float(request.form.get("temp_radiante", temp_aria))
            umidita = float(request.form.get("umidita", 0))
            vel_aria = float(request.form.get("vel_aria", 0))
            clo = float(request.form.get("clo", 0))
            met = float(request.form.get("met", 0))
            illuminazione = float(request.form.get("illuminazione", 0))
            impatto_acustico = float(request.form.get("impatto_acustico", 0))
            result = calcola_pmv_ppd(
                temp_aria, temp_radiante, vel_aria, umidita, clo, met
            )
        except ValueError:
            result = None
    return render_template(
        "index.html",
        result=result,
        temp_aria=temp_aria,
        temp_radiante=temp_radiante,
        umidita=umidita,
        vel_aria=vel_aria,
        clo=clo,
        met=met,
        illuminazione=illuminazione,
        impatto_acustico=impatto_acustico,
        spiegazioni=spiegazioni_indici,
        definizioni=parametri_definizioni,
    )


@app.route("/download")
def download():
    """Genera e restituisce il report PDF."""
    try:
        temp_aria = float(request.args.get("temp_aria", 0))
        temp_radiante = float(request.args.get("temp_radiante", temp_aria))
        vel_aria = float(request.args.get("vel_aria", 0))
        umidita = float(request.args.get("umidita", 0))
        clo = float(request.args.get("clo", 0))
        met = float(request.args.get("met", 0))
        illuminazione = float(request.args.get("illuminazione", 0))
        impatto_acustico = float(request.args.get("impatto_acustico", 0))
    except ValueError:
        abort(400, "Parametri non validi")

    res = calcola_pmv_ppd(temp_aria, temp_radiante, vel_aria, umidita, clo, met)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()
    pdf_path = genera_report_pdf(
        temp_aria,
        temp_radiante,
        vel_aria,
        umidita,
        illuminazione,
        impatto_acustico,
        met,
        clo,
        res["pmv"],
        res["ppd"],
        "Sede",  # placeholder
        "Locale",
        output_path=tmp.name,
    )

    @after_this_request
    def remove_file(response):
        try:
            os.remove(pdf_path)
        except OSError:
            pass
        return response

    return send_file(pdf_path, as_attachment=True, download_name="report.pdf")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # 10000 è la porta che userai su Render
    app.run(host="0.0.0.0", port=port)
