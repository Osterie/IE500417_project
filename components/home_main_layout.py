from dash import html, dcc
from map import create_ghg_layout

def create_main_layout(processed_data):
    return html.Div(
        className="main-graph",
        children=[
            create_title(),
            html.Div(
                className="control-grid",
                children=[
                    create_country_selection(processed_data, 'dropdown-selection', default_country='World'),
                    create_x_axis_selection(processed_data, 'dropdown-selection-x', default_x='year'),
                    create_y_axis_selection(processed_data, 'dropdown-selection-y', default_y='co2 - Mt'),
                    create_rolling_average_selection('show-rolling-average', 'rolling-window-size'),
                    create_prediction_controls('model-selection-container', 'enable-prediction', 'model-selection', 'polynomial-degree')
                ]
            ),

            html.Div(
                className="graph-card",
                children=[
                    dcc.Graph(id='graph-content')
                ]
            ),

            html.Div(
                id='slider-container',
                children=[
                    html.Label("Select year range:"),
                    dcc.RangeSlider(
                        id='year-range-slider',
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

            html.Button(
                "Show Correlation",
                id="correlation-button",
                n_clicks=0,
                style={"marginTop": "20px"}
            ),

            html.Div(
                id="correlation-output",
                style={"fontSize": "18px", "textAlign": "center", "marginTop": "10px"}
            )
        ]
    )

def create_country_selection(processed_data, dropdown_id, default_country=''):
    if not any(processed_data.country.unique() == default_country):
        default_country = ""

    return html.Div([
        html.Label("Select a country/region:"),
        dcc.Dropdown(
            processed_data.country.unique(),
            default_country,
            id= dropdown_id,
            multi=True
        )
    ])

def create_x_axis_selection(processed_data, x_axis_id, default_x=''):
    if default_x not in processed_data.columns.values:
        default_x = processed_data.columns.values[0]
    
    return html.Div([
        html.Label("X-axis attribute:"),
        dcc.Dropdown(
            processed_data.columns.values,
            default_x,
            id=x_axis_id
        )
    ])

def create_y_axis_selection(processed_data, y_axis_id, default_y=''):
    if default_y not in processed_data.columns.values:
        default_y = processed_data.columns.values[0]
    
    return html.Div([
        html.Label("Y-axis attribute:"),
        dcc.Dropdown(
            processed_data.columns.values,
            default_y,
            id=y_axis_id
        )
    ])


def create_rolling_average_selection(show_rolling_average_id, rolling_window_size_id):
    return html.Div(id='rolling-average-container', children=[
        dcc.Checklist(
            id=show_rolling_average_id,
            options=[{'label': 'Show Rolling Average', 'value': 'show'}],
            value=[],
            inline=True,
            style={"marginTop": "10px"}
        ),
        html.Div([
            html.Label("Rolling Average Window (years):"),
            dcc.Input(
                id=rolling_window_size_id,
                type='number',
                min=1,
                max=20,
                step=1,
                value=3,
                style={"width": "60px", "marginLeft": "10px"}
            )
        ], style={"marginTop": "5px"})
    ])
    
def create_prediction_controls(model_selection_container, enable_prediction_id, model_selection_id, polynomial_degree_id):
    return html.Div(id='prediction-container', children=[
        dcc.Checklist(
            id=enable_prediction_id,
            options=[{'label': 'Enable Prediction', 'value': 'predict'}],
            value=[],
            inline=True,
            style={"marginTop": "15px"}
        ),

        html.Div(
            id=model_selection_container,
            children=[
                html.Label("Regression Model:"),
                dcc.Dropdown(
                    options=[
                        {"label": "Polynomial Regression", "value": "polynomial"},
                        {"label": "Exponential", "value": "exponential"},
                        {"label": "Logarithmic", "value": "logarithmic"},
                        {"label": "Random Forest", "value": "random_forest"},
                        {"label": "LOWESS Smoother", "value": "lowess"},
                    ],
                    value="polynomial",
                    multi=True,
                    id=model_selection_id
                ),
            ],
            style={"display": "none"}
        ),

        html.Div(
            id="polynomial-degree-container",
            children=[
                html.Label("Polynomial Degree:"),
                dcc.Slider(
                    id=polynomial_degree_id,
                    min=1,
                    max=8,
                    step=1,
                    value=2,
                    marks={i: str(i) for i in range(1, 9)},
                    tooltip={"placement": "bottom", "always_visible": False},
                )
            ],
            style={"display": "none", "marginTop": "10px"}
        ),
    ])

def create_title():
    return html.H1("Visualization Tool for Seeing How the Oil and Gas Industry Relates to Emissions", style={"textAlign": "center"})