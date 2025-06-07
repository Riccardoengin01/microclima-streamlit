# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

"""Funzioni per la gestione degli oggetti smarriti."""

from __future__ import annotations

import csv
import datetime
from pathlib import Path
from typing import Dict, List, Optional


class CSVFileError(Exception):
    """Errore durante la lettura o scrittura dei file CSV."""


CAMPI_ATTIVI = [
    "id",
    "villa",
    "proprietario",
    "descrizione",
    "data_inserimento",
    "scadenza_giorni",
]

CAMPI_ARCHIVIO = CAMPI_ATTIVI + ["stato", "intestatario", "data_ritiro"]


# Utility interne


def _leggi_csv(percorso: Path, campi: List[str]) -> List[Dict[str, str]]:
    """Legge il file CSV e restituisce le righe come lista di dizionari."""
    if not percorso.exists():
        return []
    try:
        with percorso.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=campi)
            return list(reader)
    except (IOError, OSError) as exc:
        raise CSVFileError(f"Impossibile leggere il file {percorso}") from exc


def _scrivi_csv(percorso: Path, campi: List[str], righe: List[Dict[str, str]]) -> None:
    """Scrive l'elenco di dizionari nel file CSV indicato."""
    try:
        with percorso.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campi)
            writer.writerows(righe)
    except (IOError, OSError) as exc:
        raise CSVFileError(f"Impossibile scrivere il file {percorso}") from exc


def _prossimo_id(attivi: List[Dict[str, str]], archivio: List[Dict[str, str]], villa: str) -> str:
    """Calcola il prossimo ID disponibile per la villa specificata."""
    massimo = 0
    for riga in attivi + archivio:
        try:
            numero = int(riga["id"].split("-")[0])
            massimo = max(massimo, numero)
        except (KeyError, ValueError, IndexError):
            continue
    return f"{massimo + 1:03d}-VL{villa}"


# Funzioni pubbliche


def inserisci_oggetto(
    villa: str,
    proprietario: str,
    descrizione: str,
    scadenza_giorni: int = 30,
    path_attivi: str = "oggetti_attivi.csv",
    path_archivio: str = "archivio.csv",
) -> str:
    """Inserisce un oggetto e restituisce l'ID assegnato."""
    pa = Path(path_attivi)
    par = Path(path_archivio)
    attivi = _leggi_csv(pa, CAMPI_ATTIVI)
    arch = _leggi_csv(par, CAMPI_ARCHIVIO)
    nuovo_id = _prossimo_id(attivi, arch, villa)
    riga = {
        "id": nuovo_id,
        "villa": villa,
        "proprietario": proprietario,
        "descrizione": descrizione,
        "data_inserimento": datetime.date.today().isoformat(),
        "scadenza_giorni": str(scadenza_giorni),
    }
    attivi.append(riga)
    _scrivi_csv(pa, CAMPI_ATTIVI, attivi)
    return nuovo_id


def cerca_per_id(identificativo: str, path_attivi: str = "oggetti_attivi.csv") -> Optional[Dict[str, str]]:
    pa = Path(path_attivi)
    attivi = _leggi_csv(pa, CAMPI_ATTIVI)
    for riga in attivi:
        if riga.get("id") == identificativo:
            return riga
    return None


def lista_per_villa(villa: str, path_attivi: str = "oggetti_attivi.csv") -> List[Dict[str, str]]:
    pa = Path(path_attivi)
    attivi = _leggi_csv(pa, CAMPI_ATTIVI)
    return [r for r in attivi if r.get("villa") == villa]


def lista_per_proprietario(proprietario: str, path_attivi: str = "oggetti_attivi.csv") -> List[Dict[str, str]]:
    pa = Path(path_attivi)
    attivi = _leggi_csv(pa, CAMPI_ATTIVI)
    return [r for r in attivi if r.get("proprietario") == proprietario]


def ritiro_oggetto(
    identificativo: str,
    intestatario: str,
    path_attivi: str = "oggetti_attivi.csv",
    path_archivio: str = "archivio.csv",
) -> bool:
    pa = Path(path_attivi)
    par = Path(path_archivio)
    attivi = _leggi_csv(pa, CAMPI_ATTIVI)
    arch = _leggi_csv(par, CAMPI_ARCHIVIO)
    for i, riga in enumerate(attivi):
        if riga.get("id") == identificativo:
            riga_arch = riga.copy()
            riga_arch.update(
                {
                    "stato": "Ritirato",
                    "intestatario": intestatario,
                    "data_ritiro": datetime.date.today().isoformat(),
                }
            )
            arch.append(riga_arch)
            del attivi[i]
            _scrivi_csv(pa, CAMPI_ATTIVI, attivi)
            _scrivi_csv(par, CAMPI_ARCHIVIO, arch)
            return True
    return False


def archivia_oggetto(
    identificativo: str,
    stato: str = "Archiviato",
    path_attivi: str = "oggetti_attivi.csv",
    path_archivio: str = "archivio.csv",
) -> bool:
    pa = Path(path_attivi)
    par = Path(path_archivio)
    attivi = _leggi_csv(pa, CAMPI_ATTIVI)
    arch = _leggi_csv(par, CAMPI_ARCHIVIO)
    for i, riga in enumerate(attivi):
        if riga.get("id") == identificativo:
            riga_arch = riga.copy()
            riga_arch.update(
                {
                    "stato": stato,
                    "intestatario": "",
                    "data_ritiro": datetime.date.today().isoformat(),
                }
            )
            arch.append(riga_arch)
            del attivi[i]
            _scrivi_csv(pa, CAMPI_ATTIVI, attivi)
            _scrivi_csv(par, CAMPI_ARCHIVIO, arch)
            return True
    return False


def controlla_scadenze(
    path_attivi: str = "oggetti_attivi.csv",
    path_archivio: str = "archivio.csv",
    oggi: Optional[datetime.date] = None,
) -> None:
    pa = Path(path_attivi)
    par = Path(path_archivio)
    attivi = _leggi_csv(pa, CAMPI_ATTIVI)
    arch = _leggi_csv(par, CAMPI_ARCHIVIO)
    today = oggi or datetime.date.today()
    rimasti = []
    for riga in attivi:
        try:
            inserimento = datetime.date.fromisoformat(riga["data_inserimento"])
            scadenza = int(riga.get("scadenza_giorni", 30))
        except Exception:
            rimasti.append(riga)
            continue
        if (today - inserimento).days >= scadenza:
            riga_arch = riga.copy()
            riga_arch.update(
                {
                    "stato": "Smaltito",
                    "intestatario": "",
                    "data_ritiro": today.isoformat(),
                }
            )
            arch.append(riga_arch)
        else:
            rimasti.append(riga)
    _scrivi_csv(pa, CAMPI_ATTIVI, rimasti)
    _scrivi_csv(par, CAMPI_ARCHIVIO, arch)
