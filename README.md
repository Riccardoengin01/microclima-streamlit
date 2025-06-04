# Analisi del Microclima Ufficio

**Conforme alle normative UNI EN ISO 7730 e D.Lgs. 81/08**

---

## Descrizione
Questa applicazione calcola gli indici PMV (Predicted Mean Vote) e PPD (Predicted Percentage of Dissatisfied), utilizzati per valutare il comfort termico in ambienti chiusi. I calcoli sfruttano la libreria **pythermalcomfort** e rispettano le normative UNI EN ISO 7730 e il D.Lgs. 81/08.
---

## Funzionalità
- Calcolo degli indici PMV e PPD.
- Visualizzazione grafica della relazione tra PMV e PPD.
- Generazione di un report PDF con parametri e grafici.
- Controllo dei parametri ambientali con limiti predefiniti.

---

## Requisiti di Sistema
- **Python 3.8+**
- Librerie richieste:
  - `pythermalcomfort`
  - `matplotlib`
  - `fpdf`
- Tutte le dipendenze possono essere installate tramite il file `requirements.txt`.

---

## Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/Riccardoengin01/microclima-streamlit.git
   cd microclima-streamlit
   ```

2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Avvia l'applicazione:
   ```bash
   streamlit run app.py
   ```

## Formattazione del codice
Per garantire uno stile uniforme il progetto adotta **black** e **flake8**.

Esegui i controlli dalla cartella principale con:
```bash
black .
flake8
```

Assicurati che l'output non segnali errori prima di procedere con i test.

## Test
Per eseguire la suite di test automatizzati utilizziamo **pytest**.
I test andrebbero avviati solo dopo aver controllato il codice con `black` e
`flake8`.

1. Installa le dipendenze (se non lo hai già fatto):
   ```bash
   pip install -r requirements.txt
   ```
2. Avvia i test dalla cartella principale del progetto:
   ```bash
   pytest
   ```
