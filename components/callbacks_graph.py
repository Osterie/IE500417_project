from dash import Input, Output, callback
from dash.exceptions import PreventUpdate
import plotly.express as px

def register_graph_callbacks(processed_data):

    @callback(
        Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value'),
        Input('dropdown-selection-x', 'value'),
        Input('dropdown-selection-y', 'value'),
        Input('year-range-slider', 'value'),
        Input('show-rolling-average', 'value'),
        Input('rolling-window-size', 'value')
    )
    def update_graph(country, x_attr, y_attr, year_range, show_rolling, rolling_window):
        if (country is None) or (x_attr is None) or (y_attr is None):
            raise PreventUpdate

        if isinstance(country, str):
            countries = [country]
        else:
            countries = country

        dff = processed_data[processed_data.country.isin(countries)]

        if x_attr == "year":
            dff = dff[(dff['year'] >= year_range[0]) & (dff['year'] <= year_range[1])]
            fig = px.line(dff, x=x_attr, y=y_attr, color="country")

            if 'show' in show_rolling:
                for country_name in countries:
                    country_data = dff[dff['country'] == country_name].sort_values('year')
                    rolling = country_data[y_attr].rolling(window=rolling_window, min_periods=1).mean()
                    fig.add_scatter(
                        x=country_data['year'],
                        y=rolling,
                        mode='lines',
                        name=f'{country_name} - {rolling_window}-yr Rolling Avg',
                        line=dict(dash='dash')
                    )
        else:
            fig = px.scatter(dff, x=x_attr, y=y_attr, color="country")

        fig.update_layout(
            template="plotly_white",
            title=f"{y_attr} vs {x_attr}",
            title_x=0.5,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        return fig
    
    
    @callback(
        Output('rolling-average-container', 'style'),
        Input('dropdown-selection-x', 'value'),
    )
    def toggle_rolling_average(x_attr):
        if x_attr == 'year':
            return {"display": "block"}
        else:
            return {"display": "none"}
