from dash import html, dcc
from stories.price.price_data_loader import get_combined_price_data

# Get data
price_df = get_combined_price_data()

def create_price_story_layout():
    return html.Div(
        id="price-story-container",
        children=[
            html.H2("Price vs CO2 Analysis"),
            
            html.Div(
                className="controls-container",
                children=[
                    
                    html.Label("Select Country:"),
                    dcc.Dropdown(
                        id='price-dropdown',
                        options=[{'label': c, 'value': c} for c in price_df['country'].unique()],
                        value='World',
                        clearable=False
                    ),

                    
                    html.Label("Select X-axis (Price):"),
                    dcc.Dropdown(
                        id='price-dropdown-select-x',
                        options=[
                            {'label': 'Oil Price ($)', 'value': 'Oil Price ($)'},
                            {'label': 'Gas Price ($)', 'value': 'Gas Price ($)'}
                        ],
                        value='Oil Price ($)', 
                        clearable=False
                    ),

                    
                    html.Label("Select Y-axis (Emissions):"),
                    dcc.Dropdown(
                        id='price-dropdown-select-y',
                        options=[
                            {'label': 'CO2 Emissions', 'value': 'co2'}
                        ],
                        value='co2', 
                        clearable=False
                    ),
                ]
            ),

            # Graph container
            html.Div(className="graph-card", children=[
                dcc.Graph(id='price-story-graph')
            ]),

            # Slider container
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
                style={"margin-top": "20px", "padding": "0 20px"}
            ),
        ]
    )