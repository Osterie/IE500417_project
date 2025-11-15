import pandas as pd
from dash import Dash
from data_reading import preprocess_data
from components.layout import create_layout
from components.callbacks_graph import register_graph_callbacks
from components.callbacks_correlation import register_correlation_callbacks
from components.callbacks_slider import register_slider_callbacks


processed_data = pd.DataFrame()
try:
    processed_data =  pd.read_csv('data/processed_data.csv')
except FileNotFoundError:
    processed_data = preprocess_data()
    processed_data.to_csv('data/processed_data.csv', index=False)

app = Dash(__name__)
app.layout = create_layout(processed_data)

register_graph_callbacks(processed_data)
register_correlation_callbacks(processed_data)
register_slider_callbacks(processed_data)

if __name__ == "__main__":
    app.run(debug=True)

