import os
import pandas as pd
import streamlit as st


# Cache the data loading to avoid reloading on each Streamlit rerun
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return pd.DataFrame({'Timestamp': [], 'Country': [], 'GHI': [], 'DNI': [], 'DHI': []})  # Return structure if the file isn't found

    try:
        # Only load necessary columns
        cols = ['Timestamp', 'Country', 'GHI', 'DNI', 'DHI']
        data = pd.read_csv(file_path, usecols=cols)

        # Ensure Timestamp parsing and drop invalid ones
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], errors='coerce').dt.floor('s')
        data.dropna(subset=['Timestamp'], inplace=True)

        # Log success to the user
        st.info(f"Loaded {len(data)} rows of data from {file_path}.")
        
        return data
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()
