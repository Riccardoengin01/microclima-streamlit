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
from spiegazioni_indici import spiegazioni_indici, spiegazioni_indici_en
from traduzioni import LABELS


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
        LABELS["it"]["illum_ok"],
        LABELS["it"]["noise_ok"],
        data=datetime.date(2024, 1, 1),
        output_path=str(output_file),
    )
    assert pdf == str(output_file)
    assert os.path.exists(pdf)
    assert len(created) == 3
    for path in created:
        assert not os.path.exists(path)
    os.remove(pdf)


@pytest.mark.parametrize(
    "lang,spiegazioni",
    [
        ("it", spiegazioni_indici),
        ("en", spiegazioni_indici_en),
    ],
)
def test_pdf_contains_explanations(tmp_path, lang, spiegazioni):
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
        LABELS[lang]["illum_ok"],
        LABELS[lang]["noise_ok"],
        data=datetime.date(2024, 1, 1),
        output_path=str(output_file),
        lingua=lang,
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

    pmv_head = (
        (spiegazioni["pmv"].split(")")[0] + ")").replace("(", "\\(").replace(")", "\\)")
    )
    ppd_head = (
        (spiegazioni["ppd"].split(")")[0] + ")").replace("(", "\\(").replace(")", "\\)")
    )
    assert pmv_head in extracted
    assert ppd_head in extracted
    assert f"{LABELS[lang]['date']}: 2024-01-01" in extracted
    assert LABELS[lang]["lighting"].split()[0] in extracted
    assert LABELS[lang]["noise"].split()[0] in extracted
    assert LABELS[lang]["illum_ok"] in extracted
    assert LABELS[lang]["noise_ok"] in extracted
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


@pytest.mark.parametrize("lang", ["it", "en"])
def test_graphs_on_single_page(tmp_path, lang):
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
        lingua=lang,
    )
    reader = PyPDF2.PdfReader(pdf)
    assert len(reader.pages) >= 3
    page_two = reader.pages[1].extract_text()
    assert LABELS[lang]["charts_title"] in page_two
    assert LABELS[lang]["manager_signature"] in page_two
    page_three = reader.pages[2].extract_text()
    assert LABELS[lang]["light_noise_title"] in page_three
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
