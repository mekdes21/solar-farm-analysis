import pandas as pd
import streamlit as st

@st.cache
def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads the dataset and processes the Timestamp column.
    
    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Processed dataset.
    """
    data = pd.read_csv(file_path)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Convert to datetime
    return data
