import pandas as pd


def load_data():
    """
    Load the dataset from a source file.
    Returns the loaded DataFrame.
    """
    data_path = "../src/combined_solar_data.csv"
    data = pd.read_csv(data_path)
    return data


def filter_data(data, country="All", metric="GHI"):
    """
    Filter data based on user selection.
    Args:
        data: The raw data
        country: Country name or 'All' to show all data
        metric: Selected metric for visualization

    Returns:
        Filtered data subset
    """
    if country != "All":
        data = data[data["Country"] == country]
    return data
