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
        



    def get_specific_column_name(selected_y, fuel_type):
        mapping ={
            'oil_gas_consumption': {
                'oil': 'oil consumption - TWh',
                'gas': 'gas consumption - TWh'
            },
            'oil_gas_production': {
                'oil': 'oil production - TWh',
                'gas': 'gas production - TWh'
            },
            'co2 - Mt': {
                'oil': 'oil_co2 - Mt',
                'gas': 'gas_co2 - Mt'
            }
        }

        return mapping.get(selected_y, {}).get(fuel_type, None)

        

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
        


        x_axis = 'year'
        if isinstance(selected_country, str):
            selected_country = [selected_country]


        dff = price_df[price_df['country'].isin(selected_country)]
        dff = dff[(dff['year'] >= year_range[0]) & (dff['year'] <= year_range[1])]

        trendline_option = get_trendline_option(trendline_selection)
        y_axis_column = get_specific_column_name(y_axis, 'oil')

        fig = px.scatter(
            dff,
            x=x_axis,
            y=y_axis_column,
            color='Oil Price ($)',
            trendline=trendline_option,
            title=f'Oil Price vs {y_axis}',
            range_x=[year_range[0], year_range[1]]
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


        x_axis = 'year'
        if isinstance(selected_country, str):
            selected_country = [selected_country]


        dff = price_df[price_df['country'].isin(selected_country)]
        dff = dff[(dff['year'] >= year_range[0]) & (dff['year'] <= year_range[1])]

        trendline_option = get_trendline_option(trendline_selection)
        range_x = [year_range[0], year_range[1]]
        y_axis_column = get_specific_column_name(y_axis, 'gas')

        fig = px.scatter(
            dff,
            x=x_axis,
            y=y_axis_column,
            color='Gas Price ($)',
            trendline=trendline_option,
            title=f'Gas Price vs {y_axis}',
            range_x=range_x
        )
        fig.update_layout(transition_duration=500)
        return fig

        

        
        
            
   


