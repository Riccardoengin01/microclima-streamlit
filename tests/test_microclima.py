import os
import importlib.util
import sys
import pytest


def load_app(monkeypatch):
    monkeypatch.setattr(os, 'system', lambda *args, **kwargs: 0)
    root_dir = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, root_dir)
    spec = importlib.util.spec_from_file_location('app', os.path.join(root_dir, 'app.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_calcola_microclima(monkeypatch):
    app = load_app(monkeypatch)
    result = app.calcola_microclima(
        temp_aria=25,
        temp_radiante=25,
        vel_aria=0.1,
        umidita=50,
        metabolismo=1.2,
        isolamento=0.5
    )
    assert result['pmv'] == pytest.approx(0, abs=0.5)
