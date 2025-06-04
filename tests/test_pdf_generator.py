# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
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
        output_path=str(output_file),
    )
    assert pdf == str(output_file)
    assert os.path.exists(pdf)
    os.remove(pdf)
