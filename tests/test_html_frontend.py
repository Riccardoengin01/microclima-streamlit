# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

from html_frontend import app


def test_index_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    html = response.data.decode()
    assert 'name="illuminazione"' in html
    assert 'name="impatto_acustico"' in html

    response_post = client.post(
        "/",
        data={"illuminazione": "500", "impatto_acustico": "40"},
    )
    assert response_post.status_code == 200
