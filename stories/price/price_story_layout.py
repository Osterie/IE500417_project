from dash import html, dcc
from map import create_ghg_layout
from components.stacked_chart import create_stacked_chart_layout
from components.home_main_layout import (
    create_country_selection,
    create_x_axis_selection,
    create_y_axis_selection,
    create_rolling_average_selection,
    create_prediction_controls,
)

def create_price_story_layout(processed_data):
    return html.Div(
        className="main-graph",
        children=[
            
            html.P("Further down you can choose a story mode, and even further down you can view that story.", style={'margin-bottom': '60px'}),
            html.Hr(),
            
            html.H2("Story mode", style={"textAlign": "center"}),

            html.Label("Select Story mode:"),
            dcc.Dropdown(
                id="price-story-selector",
                options=["Oil dependent countries", "Gas dependent countries", "Oil producing countries", "Gas producing countries"],
                value="Oil and gas dependent countries",
                placeholder="Choose a story mode…"
            ),

            html.Hr(),
            create_price_title(),
            html.Div(
                className="control-grid",
                children=[
                    create_country_selection(processed_data, 'price-dropdown-selection', default_country='World'),
                    create_x_axis_selection(processed_data, 'price-dropdown-selection-x', default_x='year'),
                    create_y_axis_selection(processed_data, 'price-dropdown-selection-y', default_y='co2 - Mt'),
                    create_prediction_controls('price-model-selection-container', 'price-enable-prediction', 'price-model-selection', 'price-polynomial-degree')
                ]
            ),

            html.Div(
                className="price-graph-card",
                children=[
                    dcc.Graph(id='price-graph-content')
                ]
            ),
        ]
    )

def create_price_title():
    return html.H1("Price title", style={"textAlign": "center"})