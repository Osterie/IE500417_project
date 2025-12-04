from dash import Input, Output, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
from components.prediction.callbacks_prediction import add_prediction
from util import (
    create_line_chart,
    create_scatter_chart,
    get_data_for_countries,
    get_data_in_year_range,
    do_rolling_average,
    do_prediction,
)

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
    def update_graph(countries, x_attr, y_attr, year_range, show_rolling, rolling_window, prediction_mode, model_selection, poly_degree):
        if (countries is None) or (x_attr is None) or (y_attr is None):
            raise PreventUpdate

        dff = get_data_for_countries(processed_data, countries)

        if x_attr == "year":
            dff = get_data_in_year_range(dff, year_range)
            fig = create_line_chart(dff, x_attr, y_attr)

            fig = do_rolling_average(show_rolling, rolling_window, countries, dff, fig, y_attr)

            fig = do_prediction(
                prediction_mode,
                model_selection,
                processed_data,
                countries,
                x_attr,
                y_attr,
                year_range,
                poly_degree,
                fig
            )

        else:
            fig = create_scatter_chart(dff, x_attr, y_attr)

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