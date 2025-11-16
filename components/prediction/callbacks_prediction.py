# components/callbacks_prediction.py
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def add_prediction(fig, processed_data, countries, x_attr, y_attr, year_range, model_type):
    real_year_max = processed_data['year'].max()
    real_year_min = processed_data['year'].min()

    # Clamp to prevent future start year
    year_start = min(year_range[0], real_year_max)
    year_end = year_range[1]

    for c in countries:
        df_c = processed_data[processed_data["country"] == c].dropna(subset=[x_attr, y_attr])
        if len(df_c) < 2:
            continue

        x = df_c[x_attr].values.reshape(-1, 1)
        y = df_c[y_attr].values

        # Select polynomial degree
        if model_type == "linear":
            degree = 1
        elif model_type == "quadratic":
            degree = 2
        elif model_type == "cubic":
            degree = 3
        else:
            degree = 1

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

        # Add predicted line
        fig.add_trace(go.Scatter(
            x=x_pred.flatten(),
            y=y_pred,
            mode="lines",
            name=f"{c} {model_type.capitalize()} Prediction",
            line=dict(dash="dot")
        ))

    return fig
