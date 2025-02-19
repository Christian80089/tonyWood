import streamlit as st
import pandas as pd
import os

def get_csv_path(relative_path):
    """Get absolute path for a CSV file in the resources folder."""
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def load_data(input_path):
    """Load CSV data into a DataFrame."""
    try:
        csv_data = pd.read_csv(input_path)
        return csv_data
    except FileNotFoundError:
        st.error(f"❌ File non trovato: {input_path}")
        return None

# Carica i dati dai CSV
csv_paths = {
    "conteggio": get_csv_path("conteggio_query_con_totale.csv"),
    "dettagli": get_csv_path("risultati_query.csv")
}

df_main = load_data(csv_paths["conteggio"])
df_details = load_data(csv_paths["dettagli"])

# Inizializza lo stato della selezione
if "selected_type" not in st.session_state:
    st.session_state.selected_type = None

# Se i dati sono stati caricati correttamente
if df_main is not None and df_details is not None:
    st.write("### Seleziona una riga dalla tabella principale:")

    # Aggiunge una colonna per la selezione manuale
    df_main["Seleziona"] = df_main["type"].apply(lambda x: False)

    # Usa radio button per selezionare un type
    selected_type = st.radio("Seleziona un elemento:", df_main["type"].unique())

    # Salva il valore selezionato nello stato
    st.session_state.selected_type = selected_type

    st.write(f"✅ Tipo selezionato: {st.session_state.selected_type}")

    # Mostra la tabella filtrata se un tipo è stato selezionato
    if st.session_state.selected_type is not None:
        st.write(f"### Dettagli per type: {st.session_state.selected_type}")

        # Filtra la tabella dettagli
        filtered_df = df_details[df_details["type"] == st.session_state.selected_type]

        # Controlla se ci sono risultati
        if not filtered_df.empty:
            st.dataframe(filtered_df)
        else:
            st.warning("⚠️ Nessun dato trovato per il type selezionato.")
