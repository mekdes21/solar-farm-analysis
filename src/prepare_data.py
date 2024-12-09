import pandas as pd
import os

# Base directory to dynamically locate the notebooks folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set paths dynamically to datasets in the respective subfolders
benin_path = os.path.join(BASE_DIR, "../notebooks/Benin/solar_data_benin.csv")
sierra_path = os.path.join(BASE_DIR, "../notebooks/Sierra_Leone/solar_data_sierra.csv")
togo_path = os.path.join(BASE_DIR, "../notebooks/Togo/solar_data_togo.csv")

# Load datasets
try:
    benin_data = pd.read_csv(benin_path)
    sierra_data = pd.read_csv(sierra_path)
    togo_data = pd.read_csv(togo_path)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Display dataset summary
for data, name in zip([benin_data, sierra_data, togo_data], ["Benin", "Sierra Leone", "Togo"]):
    print(f"Dataset Summary for {name}")
    print(data.info(), "\n")

# Add 'Country' column to each respective DataFrame
benin_data["Country"] = "Benin"
sierra_data["Country"] = "Sierra Leone"
togo_data["Country"] = "Togo"

# Combine datasets for cross-country analysis
combined_data = pd.concat([benin_data, sierra_data, togo_data], ignore_index=True)

# Save the combined dataset for further analysis
combined_path = os.path.join(BASE_DIR, "../src/combined_solar_data.csv")
combined_data.to_csv(combined_path, index=False)

print(f"Combined dataset saved at: {combined_path}")
