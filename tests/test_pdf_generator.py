# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import os
import datetime

from pdf_generator import genera_report_pdf


def test_pdf_generation_cleanup(tmp_path):
    output_file = tmp_path / "report_microclima.pdf"
    pdf = genera_report_pdf(
        25.0,
        25.0,
        0.1,
        50.0,
        1.2,
        0.5,
        0.0,
        5.0,
        "Sede di test",
        "Locale di prova",
        data=datetime.date(2024, 1, 1),
        output_path=str(output_file),
    )
    assert pdf == str(output_file)
    assert os.path.exists(pdf)
    os.remove(pdf)


def test_pdf_contains_explanations(tmp_path):
    output_file = tmp_path / "report_microclima.pdf"
    pdf = genera_report_pdf(
        25.0,
        25.0,
        0.1,
        50.0,
        1.2,
        0.5,
        0.0,
        5.0,
        "Sede di test",
        "Locale di prova",
        data=datetime.date(2024, 1, 1),
        output_path=str(output_file),
    )
    assert pdf == str(output_file)
    with open(pdf, "rb") as file:
        data = file.read()

    import re
    import zlib

    streams = re.findall(rb"stream\n(.+?)\nendstream", data, re.DOTALL)
    extracted = ""
    for s in streams:
        try:
            extracted += zlib.decompress(s).decode("latin-1")
        except Exception:
            continue

    assert "Il PMV \\(Predicted Mean Vote\\)" in extracted
    assert "Il PPD \\(Predicted Percentage of Dissatisfied\\)" in extracted
    assert "Data: 2024-01-01" in extracted
    os.remove(pdf)


def test_pdf_has_two_pages(tmp_path):
    output_file = tmp_path / "report_microclima.pdf"
    pdf = genera_report_pdf(
        25.0,
        25.0,
        0.1,
        50.0,
        1.2,
        0.5,
        0.0,
        5.0,
        "Sede di test",
        "Locale di prova",
        data=datetime.date(2024, 1, 1),
        output_path=str(output_file),
    )
    assert pdf == str(output_file)
    with open(pdf, "rb") as file:
        content = file.read()

    assert content.count(b"/Type /Page") >= 2
    os.remove(pdf)
