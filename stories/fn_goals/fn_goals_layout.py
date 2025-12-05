from dash import html, dcc
from data_store import processed_data
from components.home_main_layout import (
    create_rolling_average_selection,
    create_prediction_controls,
)


def create_fn_story_layout():
    year_min = int(processed_data["year"].min())
    year_max = int(processed_data["year"].max())

    return html.Div(
        id="fn-story-container",
        children=[
            html.H2(
                "EU countries: oil, gas & CO₂ vs UN 2050 goals",
                style={"textAlign": "center"},
            ),

            # Top control row
            html.Div(
                className="control-grid",
                children=[
                    # Countries
                    html.Div([
                        html.Label("Select countries/regions:"),
                        dcc.Dropdown(
                            options=sorted(processed_data["country"].dropna().unique()),
                            value=["Germany", "France", "Italy", "Spain"],
                            id="fn-dropdown-selection",
                            multi=True,
                        ),
                    ]),

                    # Rolling average toggle + window
                    create_rolling_average_selection(
                        "fn-show-rolling-average",
                        "fn-rolling-window-size",
                    ),

                    # Prediction controls (enable + model dropdown + degree slider)
                    create_prediction_controls(
                        "fn-model-selection-container",
                        "fn-enable-prediction",
                        "fn-model-selection",
                        "fn-polynomial-degree",
                    ),
                ],
            ),

            # Year range slider
            html.Div(
                id="fn-slider-container",
                children=[
                    html.Label("Select year range:"),
                    dcc.RangeSlider(
                        id="fn-year-range-slider",
                        min=year_min,
                        max=year_max,
                        value=[year_min, year_max],
                        marks=None,
                        step=1,
                        allowCross=False,
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ],
                style={"marginTop": "10px"},
            ),

            # Main FN graph
            html.Div(
                className="graph-card",
                children=[
                    dcc.Graph(id="fn-graph-content"),
                ],
            ),

            # Production graph
            html.Div(
                className="graph-card",
                children=[
                    dcc.Graph(id="fn-prod-graph"),
                ],
            ),

            # Consumption graph
            html.Div(
                className="graph-card",
                children=[
                    dcc.Graph(id="fn-cons-graph"),
                ],
            ),

            html.Div(
                id="fn-goals-indicator",
                style={
                    "marginTop": "15px",
                    "fontSize": "16px",
                    "textAlign": "center",
                },
            ),
        ],
    )
