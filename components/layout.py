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
                    ]),
                    html.Div(id='rolling-average-container', children=[
                        dcc.Checklist(
                            id='show-rolling-average',
                            options=[{'label': 'Show Rolling Average', 'value': 'show'}],
                            value=[],
                            inline=True,
                            style={"marginTop": "10px"}
                        ),
                        html.Div([
                            html.Label("Rolling Average Window (years):"),
                            dcc.Input(
                                id='rolling-window-size',
                                type='number',
                                min=1,
                                max=20,
                                step=1,
                                value=3,  # default 3-year rolling average
                                style={"width": "60px", "marginLeft": "10px"}
                            )
                        ], style={"marginTop": "5px"})
                    ]),
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
