import math
import matplotlib.pyplot as plt
import tempfile

def genera_grafico_pmv_ppd(pmv, ppd):
    """Genera il grafico PMV-PPD e restituisce il percorso di un file temporaneo."""
    pmv_values = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]
    ppd_values = [100 - 95 * math.exp(-0.03353 * x ** 4 - 0.2179 * x ** 2) for x in pmv_values]

    plt.figure(figsize=(6, 4))
    plt.plot(pmv_values, ppd_values, color='red', label="PPD (%)")
    plt.axhline(10, color='black', linestyle='--', label="PPD accettabile (10%)")
    plt.axvline(pmv, color='green', linestyle='--', label=f"PMV calcolato ({pmv:.2f})")
    plt.fill_between(pmv_values, 0, ppd_values, color="cyan", alpha=0.3)
    plt.scatter([pmv], [ppd], color='black')
    plt.xlabel("PMV")
    plt.ylabel("PPD (%)")
    plt.title("Relazione tra PMV e PPD")
    plt.legend()
    plt.grid()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_file.name)
    plt.close()
    return temp_file.name
