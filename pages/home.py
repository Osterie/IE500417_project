import dash
from dash import html
from data_store import processed_data
from components.home_main_layout import create_main_layout
from map import create_ghg_layout



dash.register_page(__name__, path="/", name="Home")

def layout():
    return html.Div(
        children =[
            create_main_layout(processed_data),
            html.Hr(),
            html.Div(
                create_ghg_layout(),
                style={"marginTop": "40px"}
            )
        ]
    )