import pandas as pd
import os
from data_store import processed_data
from file_paths import FilePaths

def get_combined_price_data():
    df = processed_data.copy()

    price_data_path = FilePaths.FUEL_PRICE_INDEX.value
    if not os.path.exists(price_data_path):
        raise FileNotFoundError(f"Price data file not found at {price_data_path}")
    
    price_df = pd.read_csv(price_data_path)

    # get the oil price data (Brent)
    brent = price_df[price_df['country'] == 'Brent'][['year', 'oil spot crude price index']]
    brent = brent.rename(columns={'oil spot crude price index': 'Oil Price ($)'})

    # get gas price data (Henry Hub)
    gas = price_df[price_df['country'] == 'US Henry Hub'][['year', 'Gas price index']]
    gas = gas.rename(columns={'Gas price index': 'Gas Price ($)'})

    # merge the two datasets based on year
    df = pd.merge(df, brent, on='year', how='left')
    df = pd.merge(df, gas, on='year', how='left')

    return df
