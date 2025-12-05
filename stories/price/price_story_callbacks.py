from dash import callback, Output, Input
from plotly import express as px
from dash.exceptions import PreventUpdate
from stories.price.price_data_loader import get_combined_price_data



def register_price_story_callbacks():

    price_df = get_combined_price_data()

    @callback(
        Output('price-story-graph', 'figure'),

        Input('price-dropdown', 'value'),
        Input('price-dropdown-select-x', 'value'),
        Input('price-dropdown-select-y', 'value'),
        Input('price-year-range-slider', 'value'),
    )

    def update_price_story_graph(countries, x_attr, y_attr, year_range):
        print("Callback started!")
        if (countries is None) or (x_attr is None) or (y_attr is None):
            raise PreventUpdate
        
        if isinstance(countries, str):
            countries = [countries]


        dff = price_df[price_df['country'].isin(countries)]

        dff = dff[dff['year'].between(year_range[0], year_range[1])]

        fig = px.scatter(
            dff,
            x=x_attr,
            y=y_attr,
            color='country',
            
            title=f"{x_attr} vs {y_attr}",
        )
        fig.update_layout(transition_duration=500)
        return fig




