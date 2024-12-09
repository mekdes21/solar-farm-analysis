import os
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return pd.DataFrame({'Timestamp': [], 'Country': [], 'GHI': [], 'DNI': [], 'DHI': []})  # Return structure even if the file isn't found

    try:
        # Load data
        data = pd.read_csv(file_path)
        
        # Check if required column exists
        if 'Timestamp' not in data.columns:
            st.error("Missing 'Timestamp' column in the dataset.")
            return pd.DataFrame()

        # Parse 'Timestamp', round to remove fractional seconds
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], errors='coerce').dt.round('s')  # Round to nearest second
        data.dropna(subset=['Timestamp'], inplace=True)  # Drop rows with invalid timestamps

        # Inform the user that the data is loaded
        st.info(f"Loaded {len(data)} rows of data from {file_path}.")
        
        return data
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()
