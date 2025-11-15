from dash import Input, Output, callback
from dash.exceptions import PreventUpdate

def register_slider_callbacks(processed_data):

    @callback(
        Output('slider-container', 'style'),
        Input('dropdown-selection-x', 'value')
    )
    def toggle_slider(x_attr):
        if x_attr == 'year':
            return {"display": "block"}
        else:
            return {"display": "none"}
        
    
    @callback(
        Output('year-range-slider', 'min'),
        Output('year-range-slider', 'max'),
        Output('year-range-slider', 'value'),
        Input('dropdown-selection', 'value'),
    )
    def update_year_slider(country):
        if country is None:
            raise PreventUpdate

        if isinstance(country, str):
            countries = [country]
        else:
            countries = country

        year_mins = []
        year_maxs = []
        for country in countries:
            year_min = processed_data[processed_data['country'] == country]['year'].min()
            year_max = processed_data[processed_data['country'] == country]['year'].max()
            year_mins.append(year_min)
            year_maxs.append(year_max)

        if not year_mins or not year_maxs:
            raise PreventUpdate
        overall_min = min(year_mins)
        overall_max = max(year_maxs)

        return overall_min, overall_max, [overall_min, overall_max]