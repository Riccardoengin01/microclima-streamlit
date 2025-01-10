# Questo file fa parte del progetto Microclima-Streamlit.
#
# Microclima-Streamlit è distribuito sotto la licenza GNU General Public License v3.0.
# Puoi utilizzare, modificare e distribuire questo software secondo i termini della licenza.
#
# Per maggiori dettagli, consulta il file LICENSE o visita https://www.gnu.org/licenses/gpl-3.0.html.

# Definizioni dettagliate dei parametri
parametri_definizioni = {
    "temp_aria": """
    **Temperatura dell'aria (°C)**: 
    La temperatura dell'aria circostante misurata in gradi Celsius. 
    Questo parametro influisce sulla percezione del comfort termico.""",
    
    "temp_radiante": """
    **Temperatura radiante media (°C)**: 
    La temperatura media delle superfici circostanti che irradiano calore. 
    Include pavimenti, pareti, soffitti e oggetti presenti nell'ambiente.""",
    
    "vel_aria": """
    **Velocità dell'aria (m/s)**: 
    La velocità media dell'aria misurata in metri al secondo. 
    Un'alta velocità dell'aria può migliorare la sensazione di freschezza.""",
    
    "umidita": """
    **Umidità relativa (%)**: 
    La percentuale di umidità presente nell'aria rispetto al massimo possibile a una determinata temperatura.
    Un'elevata umidità riduce la capacità di raffreddamento della sudorazione.""",
    
    "metabolismo": """
    **Metabolismo (Met)**: 
    L'energia generata dal corpo umano in attività. 
    1 Met corrisponde a una persona seduta a riposo (~58 W/m²). 
    Valori tipici: 
    - 0.8-1.0 Met (seduto)
    - 1.5 Met (camminata leggera)
    - 4.0 Met (attività fisica intensa).""",
    
    "isolamento": """
    **Isolamento termico (Clo)**: 
    La resistenza termica fornita dall'abbigliamento. 
    1 Clo corrisponde a un abito formale completo. 
    Valori tipici:
    - 0.5 Clo (abbigliamento leggero)
    - 1.0 Clo (abbigliamento invernale)."""
}
