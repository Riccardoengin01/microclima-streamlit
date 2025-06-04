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
