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
                
                children=[
                    
                    
                    html.Div(children=[
                        html.Label("Select Country:"),
                        dcc.Dropdown(
                            id='price-dropdown',
                            options=[{'label': c, 'value': c} for c in price_df['country'].unique()],
                            value='Germany', 
                            multi=True,
                            clearable=False
                        ),
                    ]), 

                    
                    
                    html.Div(children=[
                        html.Label("Select Y-axis (Emissions):"),
                        dcc.Dropdown(
                            id='price-dropdown-select-y',
                            options=[
                                {'label': 'CO2 Emissions', 'value': 'co2 - Mt'},
                                {"label": "Oil and Gas Production", "value": "oil_gas_production"},
                                {"label": "Oil and Gas Consumption", "value": "oil_gas_consumption"}
                            ],
                            value='oil_gas_consumption', 
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
                        style={'width': '100%'},
                        children=[
                            html.H3("Oil Price Analysis"),
                            dcc.Graph(id='oil-price-graph')
                        ]
                    ),

                    
                    html.Div(
                        className="graph-container",
                        style={'width': '100%'},
                        children=[
                            html.H3("Gas Price Analysis"),
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
            ),

            html.Div(
                style={'marginTop': '40px', 'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '5px'},
                children=[
                    html.H1("Observations", style={"fontWeight": "bold", "marginBottom": "10px"}),
                    html.P(
                        "We can see that when energy prices are high (yellow dots), most countries consume less oil and gas. "
                        "However, for countries that produce oil, like Norway, this is different. "
                        "High prices often lead to more production instead of less consumption.",
                        style={"fontSize": "16px", "lineHeight": "1.5"}
                    )
                ]
            )
        ]
    )

