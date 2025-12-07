from dash import html, dcc

def create_un_prediction_controls(
    model_selection_container,
    enable_prediction_id,
    model_selection_id,
    polynomial_degree_id,
    default_enabled: bool = False,
):
    return html.Div(id='un-prediction-container', children=[
        dcc.Checklist(
            id=enable_prediction_id,
            options=[{'label': 'Enable Prediction', 'value': 'predict'}],
            value=['predict'] if default_enabled else [],
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
                    value=["polynomial"],
                    multi=True,
                    id=model_selection_id
                ),
            ],
            style={"display": "block" if default_enabled else "none"}
        ),

        html.Div(
            id="un-polynomial-degree-container",
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
