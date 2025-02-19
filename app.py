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
        st.error(f"File not found: {input_path}")
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

# Mostra la tabella principale se i dati sono stati caricati correttamente
if df_main is not None and df_details is not None:
    st.write("### Seleziona una riga dalla tabella principale:")
    selected_row = st.data_editor(df_main, num_rows="dynamic", key="table", use_container_width=True)

    # Controlla la selezione
    if selected_row is not None:
        selected_index = selected_row.get("__selected__", [])
        if selected_index:
            selected_type = df_main.iloc[selected_index[0]]["type"]
            st.session_state.selected_type = selected_type

    # Mostra la tabella filtrata se un tipo è stato selezionato
    if st.session_state.selected_type is not None:
        st.write(f"### Dettagli per type: {st.session_state.selected_type}")
        filtered_df = df_details[df_details["type"] == st.session_state.selected_type]
        st.dataframe(filtered_df)
