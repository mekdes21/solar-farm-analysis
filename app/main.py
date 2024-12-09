import streamlit as st
import datetime
from app.utils import load_data

# Constants
FILE_PATH = '../src/combined_solar_data.csv'

# Load Data
combined_data = load_data(FILE_PATH)

# Streamlit App Title
st.title("Solar Radiation Analysis Dashboard")

# Sidebar Filters
st.sidebar.title("Filters")

# Date Range Slider
date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=combined_data['Timestamp'].min().date(),
    max_value=combined_data['Timestamp'].max().date(),
    value=(combined_data['Timestamp'].min().date(), combined_data['Timestamp'].max().date()),
    format="YYYY-MM-DD"
)

# Filter Data Based on Selected Date Range
filtered_data = combined_data[
    (combined_data['Timestamp'] >= pd.Timestamp(date_range[0])) &
    (combined_data['Timestamp'] <= pd.Timestamp(date_range[1]))
]

# Tabs for Different Analyses
tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Comparative Analysis", "Summary"])

# Tab 1: Individual Analysis
with tab1:
    st.header("Individual Analysis")

    # Country Selector
    country = st.selectbox(
        "Select Country",
        options=["All"] + combined_data['Country'].unique().tolist()
    )

    # Filter by Country
    if country != "All":
        country_data = filtered_data[filtered_data["Country"] == country]
    else:
        country_data = filtered_data

    # Time-Series Visualization
    st.line_chart(country_data.set_index('Timestamp')[["GHI", "DNI", "DHI"]])

# Tab 2: Comparative Analysis
with tab2:
    st.header("Comparative Analysis")

    # Aggregate Mean Values by Country
    mean_values = filtered_data.groupby('Country').mean()[["GHI", "DNI", "DHI"]]

    # Bar Chart for Comparison
    st.bar_chart(mean_values)

# Tab 3: Summary
with tab3:
    st.header("Summary")
    st.subheader("Dataset Summary")
    st.write(filtered_data.describe())
