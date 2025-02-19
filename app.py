import streamlit as st
import pandas as pd
import os

def get_csv_path(relative_path):
    """Get absolute path for a CSV file in the resources folder."""
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def load_data(input_path):
    try:
        csv_data = pd.read_csv(input_path)
        return csv_data
    except FileNotFoundError:
        st.error("The CSV file was not found. Please check the path and try again.")
        return None
    
csv_paths = {
    "conteggio": get_csv_path(
        "conteggio_query_con_totale.csv"
    ),
    "dettagli": get_csv_path(
        "risultati_query.csv"
    )
}

df_main = load_data(csv_paths["conteggio"])
df_details = load_data(csv_paths["dettagli"])

# Stato della selezione
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

# Mostra la tabella principale
st.write("Seleziona una riga:")
selected_row = st.data_editor(df_main, num_rows="dynamic", key="table", use_container_width=True)

# Controlla la selezione
if selected_row is not None:
    selected_index = selected_row.get("__selected__", [])
    if selected_index:
        selected_id = df_main.iloc[selected_index[0]]["id"]
        st.session_state.selected_id = selected_id

# Mostra la tabella filtrata
if st.session_state.selected_id is not None:
    st.write(f"Dettagli per ID: {st.session_state.selected_id}")
    filtered_df = df_details[df_details["id"] == st.session_state.selected_id]
    st.dataframe(filtered_df)
