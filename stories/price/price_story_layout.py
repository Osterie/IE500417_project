from dash import html, dcc
from components.home_main_layout import (
    create_country_selection,
    create_x_axis_selection,
    create_y_axis_selection,
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
            
            html.Div(id='price-selected-story-mode', style={"fontWeight": "bold", "marginBottom": "200px"}),

            
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
            
            html.H1("Observations", id='price-selected-story-description-title', style={"fontWeight": "bold", "marginBottom": "20px"}),
            html.P(id='price-selected-story-description', style={"fontWeight": "bold"}),
        ]
    )

def create_price_title():
    return html.H1("Correlation between oil and gas prices with consumption and production for oil and gas producing/dependent countries", style={"textAlign": "center"})