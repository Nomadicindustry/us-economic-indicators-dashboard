import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

API_KEY = "b319bde62dfbc804466ed3acddac6231"

# List of economic indicators to pull from FRED API
SERIES = [
    ("UNRATE", "Unemployment Rate"),
    ("CPIAUCSL", "Inflation (CPI)"),
    ("FEDFUNDS", "Interest Rate")
]

all_data = []

# Loop through each economic series and standardize structure
for series_id, name in SERIES:
    
    # Build API request URL dynamically per series
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={API_KEY}&file_type=json"
    
    # Fetch data from FRED API
    response = requests.get(url)
    data = response.json()
    
    # Convert API response to DataFrame and keep relevant columns
    df = pd.DataFrame(data["observations"])
    df = df[["date", "value"]]
    
    # Convert values to numeric (handle missing or invalid values)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    
    # Add metadata for analysis and identification
    df["series_id"] = series_id
    df["indicator_name"] = name
    df["source"] = "FRED"
    df["last_updated"] = datetime.now()
    
    # Store each dataset for later combination
    all_data.append(df)

# Combine all indicators into a single dataset
final_df = pd.concat(all_data)

# Store data in SQLite database for downstream analysis (Power BI, SQL queries)
engine = create_engine("sqlite:///data/economic_data.db")
final_df.to_sql("economic_indicators", engine, if_exists="replace", index=False)

# Export to CSV for Power BI
final_df.to_csv("data/economic_data.csv", index=False)

print("Multi-series data successfully pulled and stored!")