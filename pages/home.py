import dash
from data_store import processed_data
from components.home_main_layout import create_main_layout

dash.register_page(__name__, path="/", name="Home")

def layout():
    return create_main_layout(processed_data)