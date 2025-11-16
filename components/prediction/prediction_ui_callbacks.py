from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

def register_prediction_ui_callbacks(processed_data):

    @callback(
        Output("model-selection-container", "style"),
        Output("year-range-slider", "max", allow_duplicate=True),
        Output("year-range-slider", "value", allow_duplicate=True),
        Input("enable-prediction", "value"),
        State("year-range-slider", "value"),
        prevent_initial_call="initial_duplicate"
    )
    def toggle_prediction_mode(prediction_mode, current_range):

        year_min = processed_data["year"].min()
        year_max = processed_data["year"].max()
        extend_year_max = year_max + 50

        if "predict" in prediction_mode:

            new_max = extend_year_max

            new_range = [current_range[0], min(current_range[1], new_max)]
            return {"display": "block"}, new_max, new_range
        else:

            new_max = year_max
            new_range = [max(current_range[0], year_min), min(current_range[1], new_max)]
            return {"display": "none"}, new_max, new_range
