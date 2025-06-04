# AGENTS.md
Linee guida per contribuire a **microclima-streamlit**

## 1. Commit e Pull Request
- Usa messaggi di commit concisi e in italiano, ad esempio "Aggiunge test su generazione PDF".
- Ogni pull request deve indicare chiaramente lo scopo e menzionare eventuali issue correlate.

## 2. Struttura del progetto
- I file principali del codice sono nel root: `app.py`, `layout.py`, `grafici.py`, `pdf_generator.py`.
- I test sono nella cartella `tests/` e vanno eseguiti con `pytest`.
- La documentazione principale è in `README.md`.

## 3. Formattazione e stile
- Il progetto utilizza Python 3.8+. Formatta il codice con **black** e verifica gli import con **flake8**.
- Mantieni i docstring brevi e in italiano, sul modello già presente nei file (es. `parametri_definizioni.py`).
- Evita righe oltre 120 caratteri.

## 4. Aggiunta o modifica di moduli
- Se crei nuovi moduli, posizionali nella cartella principale e aggiungi relativi test.
- Per i grafici, riusa la funzione `genera_grafico_pmv_ppd` di `grafici.py` quando possibile.

## 5. Licensing
- Tutti i file nuovi devono contenere l'intestazione di licenza GPLv3 già presente nei moduli esistenti:
  ```python
  # Questo file fa parte del progetto Microclima-Streamlit.
  #
  # Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
  # Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
  # Per dettagli: https://www.gnu.org/licenses/gpl-3.0.html
  ```

## 6. Esecuzione dei test
1. Installazione dipendenze: `pip install -r requirements.txt`
2. Avvio test: `pytest` (nella cartella principale)
3. Prima di inviare una pull request, assicurati che tutti i test passino.
