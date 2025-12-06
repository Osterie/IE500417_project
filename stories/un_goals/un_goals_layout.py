from dash import html, dcc
from stories.un_goals.un_controls import create_un_prediction_controls
from data_store import processed_data



def create_un_story_layout():
    year_min = int(processed_data["year"].min())
    year_max = int(processed_data["year"].max())

    return html.Div(
        id="un-story-container",
        children=[
            html.H2(
                "EU countries: oil, gas & Green house gasses (ghg) vs UN 2050 goals",
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
                            value=["Germany", "Netherlands", "Italy", "Spain"],
                            id="un-dropdown-selection",
                            multi=True,
                        ),
                    ]),

                    # Prediction controls (enable + model dropdown + degree slider)
                    create_un_prediction_controls(
                        "un-model-selection-container",
                        "un-enable-prediction",
                        "un-model-selection",
                        "un-polynomial-degree",
                        default_enabled=True,
                    )
                ],
            ),

            # Year range slider
            html.Div(
                id="un-slider-container",
                children=[
                    html.Label("Select year range:"),
                    dcc.RangeSlider(
                        id="un-year-range-slider",
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

            # Main un graph
            html.Div(
                className="graph-card",
                children=[
                    dcc.Graph(id="un-graph-content"),
                    html.Div(
                        className="story-text",
                        children=[
                            html.H5("What this chart shows"),
                            html.P(
                                "This chart tracks green house emissions over time for the selected countries. "
                                "with the predictions you can see an estimation of fi they will reach UN's sustainability goal."
                            )
                        ],
                        style={"marginTop": "10px"}
                    ),
                ],
            ),

            # Production graph
            html.Div(
                className="graph-card",
                children=[
                    dcc.Graph(id="un-prod-graph"),
                    html.Div(
                        className="story-text",
                        children=[
                            html.H5("What this chart shows"),
                            html.P(
                                "This chart tracks green house emissions over time for the selected countries. "
                                "with the predictions you can see an estimation of if they will reach UN's sustainability goal."
                            )
                        ],
                        style={"marginTop": "10px"}
                    ),
                ],
            ),

            # Consumption graph
            html.Div(
                className="graph-card",
                children=[
                    dcc.Graph(id="un-cons-graph"),
                    html.Div(
                        className="story-text",
                        children=[
                            html.H5("What this chart shows"),
                            html.P(
                                "This chart tracks the oil and gass consumption of the selected countries. "
                                "with the predictions you can see an estimation of fi they will reach UN's sustainability goal."
                            )
                        ],
                        style={"marginTop": "10px"}
                    ),
                ],
            ),
            

            html.Div(
                id="un-goals-indicator",
                style={
                    "marginTop": "15px",
                    "fontSize": "16px",
                    "textAlign": "center",
                },
            ),

            html.H1("Observations", style={"fontWeight": "bold", "marginBottom": "20px"}),      
            html.P('We can observe that the prediction of oil and gass production does match the sustainability goal of UN for the countries that does produce them. But the consumpiton prediction does not match the goal. There can be many causes for this, one can be that countries in FN have started producing cleaner energy, and they might also imports more oil and gass from other countries.', style={"fontWeight": "bold"}),
        ],
    )
