# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

import math
import matplotlib.pyplot as plt
import tempfile


def genera_grafico_pmv_ppd(pmv, ppd):
    """Genera il grafico PMV-PPD e restituisce il percorso di un file temporaneo."""
    pmv_values = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]
    ppd_values = [
        100 - 95 * math.exp(-0.03353 * x**4 - 0.2179 * x**2) for x in pmv_values
    ]

    plt.figure(figsize=(6, 4))
    plt.plot(pmv_values, ppd_values, color="red", label="PPD (%)")
    plt.axhline(10, color="black", linestyle="--", label="PPD accettabile (10%)")
    plt.axvline(pmv, color="green", linestyle="--", label=f"PMV calcolato ({pmv:.2f})")
    plt.fill_between(pmv_values, 0, ppd_values, color="cyan", alpha=0.3)
    plt.scatter([pmv], [ppd], color="black")
    plt.xlabel("PMV")
    plt.ylabel("PPD (%)")
    plt.title("Relazione tra PMV e PPD")
    plt.legend()
    plt.grid()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        plt.savefig(temp_file.name)
    plt.close()
    return temp_file.name


def genera_grafico_pmv_ppd_avanzato(pmv, ppd, temp_aria, umidita):
    """Crea un layout con due grafici e restituisce il file temporaneo."""
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    axes[0].scatter(temp_aria, pmv, color="blue")
    axes[0].set_xlabel("Temperatura aria (°C)")
    axes[0].set_ylabel("PMV")
    axes[0].set_title("PMV vs Temperatura")
    axes[0].axhline(0, color="gray", linestyle="--")
    axes[0].grid(True)

    axes[1].scatter(umidita, ppd, color="red")
    axes[1].set_xlabel("Umidità relativa (%)")
    axes[1].set_ylabel("PPD (%)")
    axes[1].set_title("PPD vs Umidità")
    axes[1].axhline(10, color="gray", linestyle="--")
    axes[1].grid(True)

    fig.tight_layout()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        fig.savefig(temp_file.name)
    plt.close(fig)
    return temp_file.name
