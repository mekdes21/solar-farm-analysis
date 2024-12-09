import streamlit as st
import pandas as pd
from utils import load_data
import matplotlib.pyplot as plt

# Set page layout to full screen
st.set_page_config(layout="wide")  # Ensures the app uses the full browser width

# Constants
FILE_PATH = './src/combined_solar_data.csv'

# Load Data
combined_data = load_data(FILE_PATH)

if combined_data.empty:
    st.error("Data not loaded properly. Check file path or data file.")
    st.stop()

# Streamlit App Title
st.title("Solar Radiation Analysis Dashboard")
st.markdown("""
    Explore trends in solar radiation across various countries, dates, and metrics such as GHI, DNI, DHI.
    Use the interactive filters and tabs to view visualizations and statistical insights.
""")

# Filters Section
st.header("🛠️ Filter Options")
with st.expander("Select Date Range and Country for Analysis"):
    # Sidebar-like behavior but scrollable instead
    date_range = st.date_input(
        "Select Date Range:",
        [combined_data['Timestamp'].min().date(), combined_data['Timestamp'].max().date()],
        min_value=combined_data['Timestamp'].min().date(),
        max_value=combined_data['Timestamp'].max().date()
    )
    country_filter = st.selectbox(
        "Select Country",
        options=["All"] + combined_data['Country'].unique().tolist()
    )

# Efficient Data Filtering with caching
@st.cache_data
def compute_filtered_data(data, date_range, country):
    filtered = data[
        (data['Timestamp'] >= pd.Timestamp(date_range[0])) &
        (data['Timestamp'] <= pd.Timestamp(date_range[1]))
    ]
    if country != "All":
        filtered = filtered[filtered["Country"] == country]
    return filtered


filtered_data = compute_filtered_data(combined_data, date_range, country_filter)

# Main Tabs
st.header("📊 Analysis")
tabs = st.tabs(["Individual Analysis", "Comparative Analysis", "Summary"])

# Individual Analysis
with tabs[0]:
    st.subheader("🌞 Individual Analysis")
    with st.expander("View Solar Radiation Trends for Selected Country"):
        country = st.selectbox(
            "Select Country for Analysis",
            options=["All"] + combined_data['Country'].unique().tolist()
        )
        if country != "All":
            country_data = filtered_data[filtered_data["Country"] == country]
        else:
            country_data = filtered_data
        # Resampled visualization for clarity and better performance
        downsampled_data = country_data.set_index('Timestamp')[['GHI', 'DNI', 'DHI']].resample('1D').mean().dropna()
        st.line_chart(downsampled_data)

# Comparative Analysis
with tabs[1]:
    st.subheader("🌍 Comparative Analysis")
    with st.expander("Comparison Across Multiple Countries Using Averages"):
        @st.cache_data
        def aggregate_mean(data):
            return data.groupby('Country')[['GHI', 'DNI', 'DHI']].mean()

        mean_values = aggregate_mean(filtered_data)
        st.bar_chart(mean_values)

# Summary Tab
with tabs[2]:
    st.subheader("📊 Summary Statistics")
    with st.expander("View Statistical Insights About Your Data"):
        @st.cache_data
        def compute_summary(data):
            return data.describe()

        summary_stats = compute_summary(filtered_data)
        st.write(summary_stats)

# Footer
st.markdown("---")
st.info("""
    Data visualizations powered by Streamlit.
    All solar radiation trends and insights are computed dynamically.
""")
