from dash import Input, Output, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
from components.prediction.callbacks_prediction import add_prediction

def register_graph_callbacks(processed_data):

    @callback(
        Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value'),
        Input('dropdown-selection-x', 'value'),
        Input('dropdown-selection-y', 'value'),
        Input('year-range-slider', 'value'),
        Input('show-rolling-average', 'value'),
        Input('rolling-window-size', 'value'),
        Input('enable-prediction', 'value'),
        Input('model-selection', 'value'),
        Input('polynomial-degree', 'value'),
    )
    def update_graph(country, x_attr, y_attr, year_range, show_rolling, rolling_window, prediction_mode, model_selection, poly_degree):
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

            if 'show' in (show_rolling or []):
                for country_name in countries:
                    country_data = dff[dff['country'] == country_name].sort_values('year')
                    rolling = country_data[y_attr].rolling(
                        window=rolling_window,
                        min_periods=1
                    ).mean()

                    base_color = _get_country_color(fig, country_name)

                    line_style = dict(dash='dash')
                    if base_color is not None:
                        line_style['color'] = base_color

                    fig.add_scatter(
                        x=country_data['year'],
                        y=rolling,
                        mode='lines',
                        name=f'{country_name} - {rolling_window}-yr Rolling Avg',
                        line=line_style,
                    )

            if prediction_mode and "predict" in (prediction_mode or []):
                if not model_selection:
                    selected_models = []
                elif isinstance(model_selection, str):
                    selected_models = [model_selection]
                else:
                    selected_models = model_selection

                for model_type in selected_models:
                    fig = add_prediction(
                        fig,
                        processed_data,
                        countries,
                        x_attr,
                        y_attr,
                        year_range,
                        model_type, 
                        poly_degree=poly_degree,
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

def _get_country_color(fig, country_name):
    for tr in fig.data:
        if tr.name == country_name:
            line = getattr(tr, "line", None)
            if line and getattr(line, "color", None) is not None:
                return line.color
    return None
