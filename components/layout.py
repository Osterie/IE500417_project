<<<<<<< HEAD
from dash import html, dcc
from map import create_ghg_layout
from components.stacked_chart import create_stacked_chart_layout
=======
import dash
from dash import html
>>>>>>> 6bb9a9990f8c121720088a6293dcacae2fb574d4

def create_layout():
    return html.Div(
        id="layout-container",
        children =[
            html.Div(
                id="sidebar",
                children=[
                    html.H2("Menu", style={"textAlign": "center"}),
                    html.Ul(
                        children=[
                            html.Li(html.A("Home", href="/", className="sidebar-link")),
                            html.Li(html.A("Stories", href="/stories", className="sidebar-link")),
                        ],
                        style={"listStyleType": "none", "padding": 0}
                    )
                ]
            ),
            
            html.Div(
                id="main-container",
                children=[
                    dash.page_container
                ]
            )
        ]
    )