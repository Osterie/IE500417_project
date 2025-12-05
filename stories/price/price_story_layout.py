from dash import html, dcc
from stories.price.price_data_loader import get_combined_price_data


price_df = get_combined_price_data()

def create_price_story_layout():
    return html.Div(
        id="price-story-container",
        children=[
            html.H2("Price vs CO2 Analysis"),
            
            
            html.Div(
                className="controls-container",
                
                style={'display': 'flex', 'gap': '30px', 'margin-bottom': '20px'},
                children=[
                    
                    
                    html.Div(children=[
                        html.Label("Select Country:"),
                        dcc.Dropdown(
                            id='price-dropdown',
                            options=[{'label': c, 'value': c} for c in price_df['country'].unique()],
                            value=['Germany', 'Italy','Japan'], 
                            multi=True,
                            clearable=False
                        ),
                    ]), 

                    
                    
                    html.Div(children=[
                        html.Label("Select Y-axis (Emissions):"),
                        dcc.Dropdown(
                            id='price-dropdown-select-y',
                            options=[
                                {'label': 'CO2 Emissions', 'value': 'co2 - Mt'}
                            ],
                            value='co2 - Mt', 
                            clearable=False
                        ),
                    ]), 
                    
                    
                    html.Div(children=[
                        html.Label("Select TrendLine Option:"),
                        dcc.Dropdown(
                            id="trendline-option-dropdown",
                            options=[
                                {'label': 'No Trendline', 'value': 'none'},
                                {'label': 'Show Linear Trendline (OLS)', 'value': 'ols'},
                                {'label': 'Show Local Trendline (Lowess)', 'value': 'lowess'}
                                

                            
                            ],
                            value='none',
                            clearable=False
                        )
                    ]),
                ]
            ), 

            
            
            html.Div(
                className="graph-view-container",
                style={'margin-top': '20px'},
                children=[
                    
                    html.Div(
                        className="graph-container",
                        style={'width': '45%'},
                        children=[
                            html.H3("Oil Price ($) vs CO2 Emissions"),
                            dcc.Graph(id='oil-price-graph')
                        ]
                    ),

                    
                    html.Div(
                        className="graph-container",
                        style={'width': '45%'},
                        children=[
                            html.H3("Gas Price ($) vs CO2 Emissions"),
                            dcc.Graph(id='gas-price-graph')
                        ]
                    )
                ]
            ),
            
            
            html.Div(
                children=[
                    dcc.RangeSlider(
                        id='price-year-range-slider',
                        min=price_df['year'].min(),
                        max=price_df['year'].max(),
                        value=[price_df['year'].min(), price_df['year'].max()],
                        step=1,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ],
                style={'margin-top': '30px', 'margin-left': '5px', 'margin-right': '5px'}
            )
        ]
    )