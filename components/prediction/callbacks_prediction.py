from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def register_prediction_callbacks(processed_data):

    @callback(
        Output('graph-content', 'figure', allow_duplicate=True),
        Input('enable-prediction', 'value'),
        Input('model-selection', 'value'),
        Input('dropdown-selection', 'value'),
        Input('dropdown-selection-x', 'value'),
        Input('dropdown-selection-y', 'value'),
        Input('year-range-slider', 'value'),
        prevent_initial_call='initial_duplicate'
    )
    def add_prediction(prediction_mode, model_type, country, x_attr, y_attr, year_range):

        if not prediction_mode or "predict" not in prediction_mode:
            raise PreventUpdate

        if (country is None) or (x_attr is None) or (y_attr is None):
            raise PreventUpdate

        if x_attr != "year":
            raise PreventUpdate

        countries = [country] if isinstance(country, str) else country

        real_year_min = processed_data["year"].min()
        real_year_max = processed_data["year"].max()

        year_start = min(year_range[0], real_year_max)
        year_end = year_range[1]

        fig = go.Figure()

        for c in countries:
            df_c = processed_data[processed_data["country"] == c].dropna(subset=[x_attr, y_attr])
            if len(df_c) < 2:
                continue

            x = df_c[x_attr].values.reshape(-1, 1)
            y = df_c[y_attr].values

            if model_type == "linear":
                degree = 1
            elif model_type == "quadratic":
                degree = 2
            elif model_type == "cubic":
                degree = 3
            else:
                raise PreventUpdate

            if degree > 1:
                poly = PolynomialFeatures(degree=degree)
                x_poly = poly.fit_transform(x)
                model = LinearRegression().fit(x_poly, y)
                x_pred = np.arange(year_start, year_end + 1).reshape(-1, 1)
                y_pred = model.predict(poly.transform(x_pred))
            else:
                model = LinearRegression().fit(x, y)
                x_pred = np.arange(year_start, year_end + 1).reshape(-1, 1)
                y_pred = model.predict(x_pred)

            fig.add_trace(go.Scatter(
                x=x_pred.flatten(),
                y=y_pred,
                mode="lines",
                name=f"{c} {model_type.capitalize()} Prediction",
                line=dict(dash="dot")
            ))

        return fig
