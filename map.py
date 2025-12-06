from data_store import processed_data_only_countries
from dash import html, dcc, callback, Output, Input
import plotly.express as px
from dash.exceptions import PreventUpdate

def create_ghg_layout():

    min_year=processed_data_only_countries['year'].min()
    max_year=processed_data_only_countries['year'].max()

    layout = html.Div([
        html.H1(id ='map-title', children='Y-axis attribute visualized', style={'textAlign':'center'}),

        dcc.Graph(id='ghg-map'),

        html.Div([
            html.Label("Select Year:"),
            dcc.Slider(
                id='year-slider',
                min=min_year,
                max=max_year,
                value=max_year,
                marks=None,
                step=1,
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ])
    ])
    return layout

@callback(
    Output('map-title', 'children'),
    Input('dropdown-selection-y', 'value')
)
def update_map_title(y_attr):
    if (y_attr is None) or (y_attr in ["country", "year"]):
        return "Y-axis attribute visualized"
    return f"Visualization of {y_attr} across countries (based on attribute selected on Y-axis)"


@callback(
    Output('ghg-map', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdown-selection-y', 'value')
)
def update_map(selected_year, y_attr):

    if (y_attr is None) or (y_attr in ["country", "year"]):
        raise PreventUpdate
    
    filtered_df = processed_data_only_countries[processed_data_only_countries['year'] == selected_year].copy()

    fig = px.choropleth(
        filtered_df,
        locations="country",
        locationmode='country names',
        color=y_attr,
        hover_name="country",
        projection="natural earth",
        title=f"{y_attr} in {selected_year}",
    )
    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="white",
            showcountries=True,
            countrycolor="Black"
        )
    )
    return fig