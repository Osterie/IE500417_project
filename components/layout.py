from dash import html, dcc

def create_layout(processed_data):
    return html.Div(
        id="main-container",
        children=[
            html.H1("Data Visualization", style={"textAlign": "center"}),

            html.Div(
                className="control-grid",
                children=[
                    html.Div([
                        html.Label("Select a country/region:"),
                        dcc.Dropdown(
                            processed_data.country.unique(),
                            'Canada',
                            id='dropdown-selection',
                            multi=True
                        )
                    ]),
                    html.Div([
                        html.Label("X-axis attribute:"),
                        dcc.Dropdown(
                            processed_data.columns.values,
                            'year',
                            id='dropdown-selection-x'
                        )
                    ]),
                    html.Div([
                        html.Label("Y-axis attribute:"),
                        dcc.Dropdown(
                            processed_data.columns.values,
                            'co2',
                            id='dropdown-selection-y'
                        )
                    ])
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
