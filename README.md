# Analisi ambientale ufficio


---

## Descrizione
Questa applicazione calcola gli indici PMV (Predicted Mean Vote) e PPD (Predicted Percentage of Dissatisfied), utilizzati per valutare il comfort termico in ambienti chiusi. I calcoli sfruttano la libreria **pythermalcomfort** e rispettano le normative UNI EN ISO 7730 e il D.Lgs. 81/08.
L'interfaccia principale è un'app Flask definita in `app.py`; è disponibile anche una versione Streamlit.
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
- Tutte le dipendenze principali possono essere installate tramite il file `requirements.txt`.
- I pacchetti per test e lint sono elencati in `requirements-dev.txt`.

---

## Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/Riccardoengin01/microclima-streamlit.git
   cd microclima-streamlit
   ```

2. Installa le dipendenze principali:
   ```bash
   pip install -r requirements.txt
   ```

3. Installa le dipendenze per test e lint:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Avvia l'interfaccia Flask:
   ```bash
   python app.py
   ```

5. Oppure avvia la versione Streamlit:
   ```bash
   streamlit run streamlit_main.py
   # oppure
   streamlit run streamlit_app.py
   ```

### Frontend HTML (alternativa)
In alternativa all'interfaccia Streamlit puoi eseguire un semplice frontend HTML basato su Flask:

```bash
python html_frontend.py
```

Per cambiare l'interfaccia modifica il file `templates/index.html` e riavvia il server dopo aver salvato le modifiche.


Le definizioni dei parametri mostrati nella pagina provengono dal file `parametri_definizioni.py`.
Le spiegazioni di PMV e PPD sono contenute in `spiegazioni_indici.py`.
Dopo il calcolo compare il pulsante **Scarica Report PDF**, gestito dall'endpoint `/download` che restituisce il documento.
Esempio di richiesta:
```bash
curl "http://localhost:5000/download?temp_aria=25&temp_radiante=25&vel_aria=0.1&umidita=50&clo=0.5&met=1.2&illuminazione=500&impatto_acustico=40" -o report.pdf
```
## Ambiente di sviluppo
Per preparare l'ambiente prima di avviare i test installa tutte le dipendenze
Python:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
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
elencate in `requirements.txt` e `requirements-dev.txt`:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
Questi comandi installano anche `pytest`, necessario per avviare la suite di test.

Terminata l'installazione puoi eseguire i test con:

```bash
pytest
```

## Test
Per eseguire la suite di test automatizzati utilizziamo **pytest**.
I test andrebbero avviati solo dopo aver controllato il codice con `black` e
`flake8`.

1. Installa le dipendenze (se non lo hai già fatto):
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
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
The main interface is a Flask app defined in `app.py`; a Streamlit version is also available.

### Features
- Calculation of PMV and PPD indices.
- Graphical visualization of the relationship between PMV and PPD.
- Generation of a PDF report with parameters and charts.
- The PDF also includes an advanced plot with PMV vs temperature and PPD vs humidity.
- Environmental parameters check with predefined limits.
- Recommended ranges are 300-1000 lux for lighting and 30-55 dB for noise.

### Environmental parameters
- Adequate lighting improves concentration and reduces eye strain.
- Excessive noise can cause stress and divert attention.

### System Requirements
- **Python 3.8+**
- Required libraries:
  - `pythermalcomfort`
  - `matplotlib`
  - `fpdf`
- All main dependencies can be installed via the `requirements.txt` file.
- Packages for testing and linting are listed in `requirements-dev.txt`.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Riccardoengin01/microclima-streamlit.git
   cd microclima-streamlit
   ```

2. Install main dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install test and lint dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Start the Flask interface:
   ```bash
   python app.py
   ```

5. Or launch the Streamlit version:
   ```bash
   streamlit run streamlit_main.py
   # or
   streamlit run streamlit_app.py
   ```

### HTML Frontend (alternative)
As an alternative to the Streamlit interface you can run a simple Flask-based HTML frontend:

```bash
python html_frontend.py
```

To change the interface edit `templates/index.html` and restart the server after saving.


Parameter definitions displayed in the page are stored in `parametri_definizioni.py`.
Explanations for PMV and PPD are provided in `spiegazioni_indici.py`.
After submitting the form a **Download PDF Report** button appears; it calls the `/download` endpoint to generate the document.
Example request:
```bash
curl "http://localhost:5000/download?temp_aria=25&temp_radiante=25&vel_aria=0.1&umidita=50&clo=0.5&met=1.2&illuminazione=500&impatto_acustico=40" -o report.pdf
```
### Development environment
Before running the tests install all Python dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
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
Before running `pytest` it is essential to install all dependencies listed in `requirements.txt` and `requirements-dev.txt`:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
These commands also install `pytest`, needed to run the test suite.

After installing the dependencies you can run the tests with:

```bash
pytest
```

### Tests
We use **pytest** to run the automated test suite. Tests should be run only after the code has been checked with `black` and `flake8`.

1. Install the dependencies (if you haven't already):
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
2. Run the tests from the project root:
   ```bash
   pytest
   ```

### Continuous integration
Tests and formatting checks are automatically executed through GitHub Actions on every push or pull request.
