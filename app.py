import pandas as pd
from dash import Dash
from components.layout import create_layout
from components.tabs import create_tabs_layout
from components.callbacks_graph import register_graph_callbacks
from components.callbacks_correlation import register_correlation_callbacks
from components.callbacks_slider import register_slider_callbacks
from components.prediction.prediction_ui_callbacks import register_prediction_ui_callbacks
from data_store import processed_data


app = Dash(__name__, use_pages=True)
server = app.server

from components.layout import create_layout

app.layout = create_layout()

register_graph_callbacks(processed_data)
register_correlation_callbacks(processed_data)
register_slider_callbacks(processed_data)
register_prediction_ui_callbacks(processed_data)

app.processed_data = processed_data

if __name__ == "__main__":
    app.run(debug=True)

