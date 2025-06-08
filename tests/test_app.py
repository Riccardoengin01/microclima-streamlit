import io

import pytest
from PyPDF2 import PdfReader

from app import app
from spiegazioni_indici import spiegazioni_indici


@pytest.fixture()
def client():
    return app.test_client()


def test_index_shows_explanations_and_button(client):
    data = {
        "temp_aria": "25",
        "temp_radiante": "25",
        "umidita": "50",
        "vel_aria": "0.1",
        "clo": "0.5",
        "met": "1.2",
        "illuminazione": "500",
        "impatto_acustico": "40",
    }
    resp = client.post("/", data=data)
    assert resp.status_code == 200
    html = resp.data.decode()
    assert "Scarica Report PDF" in html
    assert spiegazioni_indici["pmv"] in html
    assert "Definizioni parametri" in html
    assert "Temperatura dell&#39;aria" in html


def test_download_generates_pdf(client):
    params = {
        "temp_aria": "25",
        "temp_radiante": "25",
        "vel_aria": "0.1",
        "umidita": "50",
        "clo": "0.5",
        "met": "1.2",
        "illuminazione": "500",
        "impatto_acustico": "40",
    }
    resp = client.get("/download", query_string=params)
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/pdf"
    PdfReader(io.BytesIO(resp.data))
