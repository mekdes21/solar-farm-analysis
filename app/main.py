import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from app.utils import load_data, filter_data


# Title
st.title("🌞 Solar Radiation Analysis Dashboard")

# Load data
data = load_data()

# Sidebar Interactivity
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Select Country", ["All", "Benin", "Sierra Leone", "Togo"])
metric = st.sidebar.selectbox("Select Metric", ["GHI", "DNI", "DHI"])

# Filter data based on selection
filtered_data = filter_data(data, country, metric)

# Line chart visualization
st.subheader("Solar Radiation Over Time")
st.line_chart(
    filtered_data.set_index("Timestamp")[metric],
    use_container_width=True
)

# Additional visualizations with Seaborn
st.subheader("Visual Insights")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x="Timestamp", y=metric, data=filtered_data, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
