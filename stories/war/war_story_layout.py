from dash import html, dcc
from components.home_main_layout import create_main_layout
from data_store import processed_data
from stories.war.wars import wars
from components.home_main_layout import (
    create_country_selection,
    create_x_axis_selection,
    create_y_axis_selection,
    create_rolling_average_selection,
    create_prediction_controls,
)

def create_war_story_layout():
    
    x_axis_values = [
        "year",
    ]
    
    y_axis_values = [
        "oil production - TWh",
        "gas production - TWh",
        "oil consumption - TWh",
        "gas consumption - TWh",
        "co2",
        "gas_co2",
        "oil_co2"
    ]
    
    
    processed_data_x_axis = processed_data[x_axis_values]
    processed_data_y_axis = processed_data[y_axis_values]
    
    return html.Div(
        id="war-story-container",
        children=[
            html.Hr(),
            
            html.H2("Story mode", style={"textAlign": "center"}),

            html.Label("Select Story mode:"),
            dcc.Dropdown(
                id="war-story-selector",
                options=["Self-Exploration", "Global Conflicts", "Iraq Wars"],
                value="Self-Exploration",
                placeholder="Choose a story mode…"
            ),

            html.Hr(),


            html.Div(id='war-selected-story-mode', style={"fontWeight": "bold", "marginBottom": "200px"}),
            
            
            html.H2("How Wars Affect Oil & Gas", style={"textAlign": "center"}),

            html.Label("Select war(s):"),
            dcc.Dropdown(
                id="war-selector",
                options=[{"label": v["name"], "value": k} for k, v in wars.items()],
                multi=True,
                placeholder="Choose wars to overlay…"
            ),


            html.Div(
                className="control-grid",
                children=[
                    create_country_selection(processed_data, 'war-dropdown-selection', default_country='World'),
                    create_x_axis_selection(processed_data_x_axis, 'war-dropdown-selection-x', default_x='year'),
                    create_y_axis_selection(processed_data_y_axis, 'war-dropdown-selection-y', default_y='oil production - TWh'),
                    create_rolling_average_selection('war-show-rolling-average', 'war-rolling-window-size'),
                    create_prediction_controls('war-model-selection-container', 'war-enable-prediction', 'war-model-selection', 'war-polynomial-degree')
                ]
            ),

            html.Div(
                className="graph-card",
                children=[
                    dcc.Graph(id='war-graph-content')
                ]
            ),

            html.Div(
                id='war-slider-container',
                children=[
                    html.Label("Select year range:"),
                    dcc.RangeSlider(
                        id='war-year-range-slider',
                        min=processed_data['year'].min(),
                        max=processed_data['year'].max(),
                        value=[
                            processed_data['year'].min(),
                            processed_data['year'].max()
                        ],
                        marks=None,
                        step=1,
                        allowCross=False,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ],
                style={"display": "none"}
            ),
            
            html.H2("Observations", id='war-selected-story-description-title', style={"fontWeight": "bold", "marginBottom": "20px"}),
            html.Div(id='war-selected-story-description', style={"fontWeight": "bold"}),
        ]
    )