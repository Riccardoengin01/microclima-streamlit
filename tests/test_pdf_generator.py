import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from pdf_generator import genera_report_pdf


def test_pdf_generation_cleanup(tmp_path):
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
    )
    assert os.path.exists(pdf)
    os.remove(pdf)
