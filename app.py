import streamlit as st
import pandas as pd

# Dati di esempio
df_main = pd.read_csv("C:/Users/chris/Desktop/tonyWoodScript/conteggio_query_con_totale.csv", delimiter=",")

df_details = pd.read_csv("C:/Users/chris/Desktop/tonyWoodScript/risultati_query.csv", delimiter=",")

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
