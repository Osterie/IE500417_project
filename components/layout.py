import dash
from dash import html


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