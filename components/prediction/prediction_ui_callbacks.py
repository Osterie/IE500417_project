from dash import Input, Output, State, callback

def register_prediction_ui_callbacks(processed_data):

    @callback(
        Output("model-selection-container", "style"),
        Output("year-range-slider", "max", allow_duplicate=True),
        Output("year-range-slider", "value", allow_duplicate=True),
        Input("enable-prediction", "value"),
        Input("dropdown-selection-x", "value"), 
        State("year-range-slider", "value"),
        prevent_initial_call="initial_duplicate",
    )
    def toggle_prediction_mode(prediction_mode, x_attr, current_range):
        year_min = processed_data["year"].min()
        year_max = processed_data["year"].max()
        extend_year_max = year_max + 50

        if current_range is None:
            current_range = [year_min, year_max]

        # Only manipulate the year slider if we're actually using year on X
        if x_attr != "year":
            # Just show/hide model UI, don't touch slider
            if prediction_mode and "predict" in prediction_mode:
                return {"display": "block"}, year_max, current_range
            return {"display": "none"}, year_max, current_range

        # Original year behavior
        if prediction_mode and "predict" in prediction_mode:
            new_max = extend_year_max
            new_range = current_range
            return {"display": "block"}, new_max, new_range
        else:
            new_max = year_max
            new_range = [
                max(current_range[0], year_min),
                min(current_range[1], new_max)
            ]
            return {"display": "none"}, new_max, new_range

    @callback(
        Output("polynomial-degree-container", "style"),
        Input("model-selection", "value"),
        Input("enable-prediction", "value"),
    )
    def toggle_polynomial_degree(model_selection, prediction_mode):
        if not (prediction_mode and "predict" in prediction_mode):
            return {"display": "none", "marginTop": "10px"}

        if not model_selection:
            return {"display": "none", "marginTop": "10px"}

        selected = model_selection if isinstance(model_selection, list) else [model_selection]

        if "polynomial" in selected:
            return {"display": "block", "marginTop": "10px"}

        return {"display": "none", "marginTop": "10px"}
