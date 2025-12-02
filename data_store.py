import pandas as pd
from data_reading import preprocess_data

try:
    processed_data = pd.read_csv('data/processed_data.csv')
except FileNotFoundError:
    processed_data = preprocess_data()
    processed_data.to_csv('data/processed_data.csv', index=False)
