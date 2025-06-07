# Analisi ambientale ufficio


---

## Descrizione
Questa applicazione calcola gli indici PMV (Predicted Mean Vote) e PPD (Predicted Percentage of Dissatisfied), utilizzati per valutare il comfort termico in ambienti chiusi. I calcoli sfruttano la libreria **pythermalcomfort** e rispettano le normative UNI EN ISO 7730 e il D.Lgs. 81/08.
---

## Funzionalità
- Calcolo degli indici PMV e PPD.
- Visualizzazione grafica della relazione tra PMV e PPD.
- Generazione di un report PDF con parametri e grafici.
- Il PDF include anche un grafico avanzato con PMV vs temperatura e PPD vs umidità.
- Controllo dei parametri ambientali con limiti predefiniti.
- Le soglie consigliate sono 300-1000 lux per l'illuminazione e 30-55 dB per il rumore.

### Parametri ambientali
- Un'adeguata illuminazione migliora la concentrazione e riduce l'affaticamento visivo.
- Un eccessivo rumore può generare stress e distogliere l'attenzione.

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

### Frontend HTML (alternativa)
In alternativa all'interfaccia Streamlit puoi eseguire un semplice frontend HTML basato su Flask:

```bash
python html_frontend.py
```

Per cambiare l'interfaccia modifica il file `templates/index.html` e riavvia il server dopo aver salvato le modifiche.

## Ambiente di sviluppo
Per preparare l'ambiente prima di avviare i test installa tutte le dipendenze
Python:

```bash
pip install -r requirements.txt
```
Se utilizzi un ambiente containerizzato, i pacchetti di sistema indicati nel
file `packages.txt` verranno installati automaticamente tramite la
configurazione presente nella cartella `.devcontainer`. La stessa configurazione
provvede anche a installare i moduli Python elencati in `requirements.txt`.

## Formattazione del codice
Per garantire uno stile uniforme il progetto adotta **black** e **flake8**.

Esegui i controlli dalla cartella principale con:
```bash
black .
flake8
```

Assicurati che l'output non segnali errori prima di procedere con i test.

## Preparazione ai test
Prima di lanciare `pytest` è fondamentale installare tutte le dipendenze
elencate in `requirements.txt`:

```bash
pip install -r requirements.txt
```
Questo comando installa anche `pytest`, necessario per avviare la suite di test.

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

## Integrazione continua
I test e i controlli di formattazione vengono eseguiti automaticamente
tramite GitHub Actions ad ogni push o pull request.

---

## English version

### Description
This application calculates the PMV (Predicted Mean Vote) and PPD (Predicted Percentage of Dissatisfied) indices used to evaluate indoor thermal comfort. Calculations rely on the **pythermalcomfort** library and comply with UNI EN ISO 7730 and Italian D.Lgs. 81/08.

### Features
- Calculation of PMV and PPD indices.
- Graphical visualization of the relationship between PMV and PPD.
- Generation of a PDF report with parameters and charts.
- The PDF also includes an advanced plot with PMV vs temperature and PPD vs humidity.
- Environmental parameters check with predefined limits.

### System Requirements
- **Python 3.8+**
- Required libraries:
  - `pythermalcomfort`
  - `matplotlib`
  - `fpdf`
- All dependencies can be installed via the `requirements.txt` file.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Riccardoengin01/microclima-streamlit.git
   cd microclima-streamlit
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

### HTML Frontend (alternative)
As an alternative to the Streamlit interface you can run a simple Flask-based HTML frontend:

```bash
python html_frontend.py
```

To change the interface edit `templates/index.html` and restart the server after saving.

### Development environment
Before running the tests install all Python dependencies:

```bash
pip install -r requirements.txt
```
If you use a containerized environment, the system packages listed in `packages.txt` will be installed automatically via the `.devcontainer` configuration. The same configuration also installs the Python modules listed in `requirements.txt`.

### Code formatting
To ensure a consistent style the project adopts **black** and **flake8**.

Run the checks from the project root:
```bash
black .
flake8
```

Make sure the output does not report errors before continuing with the tests.

### Test preparation
Before running `pytest` it is essential to install all dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```
This command also installs `pytest`, needed to run the test suite.

### Tests
We use **pytest** to run the automated test suite. Tests should be run only after the code has been checked with `black` and `flake8`.

1. Install the dependencies (if you haven't already):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the tests from the project root:
   ```bash
   pytest
   ```

### Continuous integration
Tests and formatting checks are automatically executed through GitHub Actions on every push or pull request.
