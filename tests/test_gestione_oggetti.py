# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import csv
import datetime
from pathlib import Path

import gestione_oggetti
from gestione_oggetti import (
    archivia_oggetto,
    cerca_per_id,
    controlla_scadenze,
    inserisci_oggetto,
    lista_per_proprietario,
    lista_per_villa,
    ritiro_oggetto,
)
import pytest


def leggi(path: Path, campi):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, fieldnames=campi))


def test_id_progressivo(tmp_path):
    active = tmp_path / "attivi.csv"
    archive = tmp_path / "archivio.csv"
    id1 = inserisci_oggetto(
        "1", "Mario", "Borsa", path_attivi=str(active), path_archivio=str(archive)
    )
    id2 = inserisci_oggetto(
        "2", "Luca", "Chiavi", path_attivi=str(active), path_archivio=str(archive)
    )
    assert id1 == "001-VL1"
    assert id2 == "002-VL2"


def test_ricerca_e_lista(tmp_path):
    active = tmp_path / "attivi.csv"
    archive = tmp_path / "archivio.csv"
    oid = inserisci_oggetto(
        "1", "Mario", "Borsa", path_attivi=str(active), path_archivio=str(archive)
    )
    assert cerca_per_id(oid, str(active))["proprietario"] == "Mario"
    assert lista_per_villa("1", str(active))[0]["id"] == oid
    assert lista_per_proprietario("Mario", str(active))[0]["id"] == oid


def test_ritiro(tmp_path):
    active = tmp_path / "attivi.csv"
    archive = tmp_path / "archivio.csv"
    oid = inserisci_oggetto(
        "1", "Mario", "Borsa", path_attivi=str(active), path_archivio=str(archive)
    )
    assert ritiro_oggetto(oid, "MarioR", str(active), str(archive))
    attivi = leggi(
        active,
        [
            "id",
            "villa",
            "proprietario",
            "descrizione",
            "data_inserimento",
            "scadenza_giorni",
        ],
    )
    arch = leggi(
        archive,
        [
            "id",
            "villa",
            "proprietario",
            "descrizione",
            "data_inserimento",
            "scadenza_giorni",
            "stato",
            "intestatario",
            "data_ritiro",
        ],
    )
    assert not attivi
    assert arch[0]["stato"] == "Ritirato"
    assert arch[0]["intestatario"] == "MarioR"


def test_archiviazione_manuale(tmp_path):
    active = tmp_path / "attivi.csv"
    archive = tmp_path / "archivio.csv"
    oid = inserisci_oggetto(
        "1", "Mario", "Borsa", path_attivi=str(active), path_archivio=str(archive)
    )
    assert archivia_oggetto(oid, "Perso", str(active), str(archive))
    attivi = leggi(
        active,
        [
            "id",
            "villa",
            "proprietario",
            "descrizione",
            "data_inserimento",
            "scadenza_giorni",
        ],
    )
    arch = leggi(
        archive,
        [
            "id",
            "villa",
            "proprietario",
            "descrizione",
            "data_inserimento",
            "scadenza_giorni",
            "stato",
            "intestatario",
            "data_ritiro",
        ],
    )
    assert not attivi
    assert arch[0]["stato"] == "Perso"


def test_controllo_scadenze(tmp_path):
    active = tmp_path / "attivi.csv"
    archive = tmp_path / "archivio.csv"
    inserisci_oggetto(
        "1", "Mario", "Borsa", path_attivi=str(active), path_archivio=str(archive)
    )
    rows = leggi(
        active,
        [
            "id",
            "villa",
            "proprietario",
            "descrizione",
            "data_inserimento",
            "scadenza_giorni",
        ],
    )
    rows[0]["data_inserimento"] = (
        datetime.date.today() - datetime.timedelta(days=31)
    ).isoformat()
    with active.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "villa",
                "proprietario",
                "descrizione",
                "data_inserimento",
                "scadenza_giorni",
            ],
        )
        writer.writerows(rows)
    controlla_scadenze(str(active), str(archive), oggi=datetime.date.today())
    attivi = leggi(
        active,
        [
            "id",
            "villa",
            "proprietario",
            "descrizione",
            "data_inserimento",
            "scadenza_giorni",
        ],
    )
    arch = leggi(
        archive,
        [
            "id",
            "villa",
            "proprietario",
            "descrizione",
            "data_inserimento",
            "scadenza_giorni",
            "stato",
            "intestatario",
            "data_ritiro",
        ],
    )
    assert not attivi
    assert arch[0]["stato"] == "Smaltito"


def test_scrittura_csv_error(tmp_path, monkeypatch):
    active = tmp_path / "attivi.csv"
    archive = tmp_path / "archivio.csv"

    def fake_open(self, *args, **kwargs):
        raise OSError("fail")

    monkeypatch.setattr(Path, "open", fake_open)
    with pytest.raises(gestione_oggetti.CSVFileError):
        inserisci_oggetto(
            "1",
            "Mario",
            "Borsa",
            path_attivi=str(active),
            path_archivio=str(archive),
        )
