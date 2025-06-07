# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import os
import datetime
import tempfile

import grafici
import pdf_generator
from fpdf import FPDF
import pytest
import PyPDF2

from pdf_generator import genera_report_pdf


def test_pdf_generation_cleanup(tmp_path, monkeypatch):
    created = []
    original = tempfile.NamedTemporaryFile

    def fake_tempfile(*args, **kwargs):
        kwargs["delete"] = False
        kwargs["suffix"] = ".png"
        kwargs["dir"] = tmp_path
        f = original(**kwargs)
        created.append(f.name)
        return f

    monkeypatch.setattr(grafici.tempfile, "NamedTemporaryFile", fake_tempfile)

    output_file = tmp_path / "report_microclima.pdf"
    pdf = genera_report_pdf(
        25.0,
        25.0,
        0.1,
        50.0,
        500.0,
        45.0,
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
    assert len(created) == 3
    for path in created:
        assert not os.path.exists(path)
    os.remove(pdf)


def test_pdf_contains_explanations(tmp_path):
    output_file = tmp_path / "report_microclima.pdf"
    pdf = genera_report_pdf(
        25.0,
        25.0,
        0.1,
        50.0,
        500.0,
        45.0,
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
    assert "Illuminazione" in extracted
    assert "Impatto acustico" in extracted
    os.remove(pdf)


def test_pdf_has_three_pages(tmp_path):
    output_file = tmp_path / "report_microclima.pdf"
    pdf = genera_report_pdf(
        25.0,
        25.0,
        0.1,
        50.0,
        500.0,
        45.0,
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

    assert content.count(b"/Type /Page") >= 3
    os.remove(pdf)


def test_graphs_on_single_page(tmp_path):
    output_file = tmp_path / "report_microclima.pdf"
    pdf = genera_report_pdf(
        25.0,
        25.0,
        0.1,
        50.0,
        500.0,
        45.0,
        1.2,
        0.5,
        0.0,
        5.0,
        "Sede di test",
        "Locale di prova",
        data=datetime.date(2024, 1, 1),
        output_path=str(output_file),
    )
    reader = PyPDF2.PdfReader(pdf)
    assert len(reader.pages) >= 3
    page_two = reader.pages[1].extract_text()
    assert "Grafici PMV-PPD" in page_two
    assert "Firma del responsabile" in page_two
    page_three = reader.pages[2].extract_text()
    assert "Illuminazione e Rumore" in page_three
    os.remove(pdf)


def test_comment_and_signature_present(tmp_path):
    output_file = tmp_path / "report_microclima.pdf"
    pdf = genera_report_pdf(
        25.0,
        25.0,
        0.1,
        50.0,
        500.0,
        45.0,
        1.2,
        0.5,
        0.0,
        5.0,
        "Sede di test",
        "Locale di prova",
        "Test commento",
        "Mario Rossi",
        data=datetime.date(2024, 1, 1),
        output_path=str(output_file),
    )
    reader = PyPDF2.PdfReader(pdf)
    page_two = reader.pages[1].extract_text()
    assert "Test commento" in page_two
    assert "Mario Rossi" in page_two
    os.remove(pdf)


def test_pdf_generation_error(tmp_path, monkeypatch):
    def fake_output(self, *args, **kwargs):
        raise IOError("fail")

    monkeypatch.setattr(FPDF, "output", fake_output)
    with pytest.raises(pdf_generator.PdfGenerationError):
        genera_report_pdf(
            25.0,
            25.0,
            0.1,
            50.0,
            500.0,
            45.0,
            1.2,
            0.5,
            0.0,
            5.0,
            "Sede",
            "Locale",
            output_path=str(tmp_path / "out.pdf"),
        )
