# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import math
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app import calcola_microclima


def test_calcola_microclima_iso():
    res = calcola_microclima(25.0, 25.0, 0.1, 50.0, 1.2, 0.5)
    assert math.isfinite(res["pmv"])
    assert math.isfinite(res["ppd"])
    assert -3.0 <= res["pmv"] <= 3.0
    assert 0 <= res["ppd"] <= 100
