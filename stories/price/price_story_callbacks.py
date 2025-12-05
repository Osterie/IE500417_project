from dash import callback, Output, Input
from plotly import express as px
from dash.exceptions import PreventUpdate
from stories.price.price_data_loader import get_combined_price_data



def register_price_story_callbacks():

    price_df = get_combined_price_data()


    def get_trendline_option(trendline_selection):
        if trendline_selection == 'none':
            return None
        elif trendline_selection == 'ols':
            return 'ols'
        elif trendline_selection == 'lowess':
            return 'lowess'
        else:
            return None
        

    @callback(
        Output('oil-price-graph', 'figure'),
        Input('price-dropdown', 'value'),
        Input('price-dropdown-select-y', 'value'),
        Input('price-year-range-slider', 'value'),
        Input('trendline-option-dropdown', 'value')
    )

    def update_oil_price_graph(selected_country, y_axis, year_range, trendline_selection):
        if (not selected_country) or (len(selected_country) == 0) or (y_axis is None):
            return px.scatter(title="Please select at least one country and a Y-axis option.")
        


        x_axis = 'Oil Price ($)'
        if isinstance(selected_country, str):
            selected_country = [selected_country]


        dff = price_df[price_df['country'].isin(selected_country)]
        dff = dff[(dff['year'] >= year_range[0]) & (dff['year'] <= year_range[1])]

        trendline_option = get_trendline_option(trendline_selection)

        fig = px.scatter(
            dff,
            x=x_axis,
            y=y_axis,
            color='country',
            trendline=trendline_option,
            title='Oil Price vs Emissions',
        )
        fig.update_layout(transition_duration=500)
        return fig




    @callback(
        Output('gas-price-graph', 'figure'),
        Input('price-dropdown', 'value'),
        Input('price-dropdown-select-y', 'value'),
        Input('price-year-range-slider', 'value'),
        Input('trendline-option-dropdown', 'value')
    )

    def update_gas_graph(selected_country, y_axis, year_range, trendline_selection):
        if (not selected_country) or (len(selected_country) == 0) or (y_axis is None):
            return px.scatter(title="Please select at least one country and a Y-axis option.")


        x_axis = 'Gas Price ($)'
        if isinstance(selected_country, str):
            selected_country = [selected_country]


        dff = price_df[price_df['country'].isin(selected_country)]
        dff = dff[(dff['year'] >= year_range[0]) & (dff['year'] <= year_range[1])]

        trendline_option = get_trendline_option(trendline_selection)

        fig = px.scatter(
            dff,
            x=x_axis,
            y=y_axis,
            color='country',
            trendline=trendline_option,
            title='Gas Price vs Emissions',
        )
        fig.update_layout(transition_duration=500)
        return fig

        

        
        
            
   


