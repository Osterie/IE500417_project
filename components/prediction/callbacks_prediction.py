import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor

try:
    from statsmodels.nonparametric.smoothers_lowess import lowess # type: ignore
    _HAS_LOWESS = True
except ImportError:
    _HAS_LOWESS = False


def _fit_polynomial(x, y, x_pred, degree):
    if degree == 1:
        model = LinearRegression().fit(x, y)
        return model.predict(x_pred)

    poly = PolynomialFeatures(degree=degree, include_bias=True)
    x_poly = poly.fit_transform(x)
    model = LinearRegression().fit(x_poly, y)
    x_pred_poly = poly.transform(x_pred)
    return model.predict(x_pred_poly)


def _get_country_color(fig, country_name):
    for tr in fig.data:
        if tr.name == country_name:
            line = getattr(tr, "line", None)
            if line and getattr(line, "color", None) is not None:
                return line.color
    return None


def add_prediction(
    fig,
    processed_data,
    countries,
    x_attr,
    y_attr,
    year_range,
    model_type,
    poly_degree=None,
):
    real_year_min = processed_data["year"].min()
    real_year_max = processed_data["year"].max()

    year_start = min(year_range[0], real_year_max)
    year_end = year_range[1]
    if year_end < year_start:
        year_end = year_start

    x_pred = np.arange(year_start, year_end + 1).reshape(-1, 1)

    base_styles = {
        "polynomial":   dict(dash="dot",      width=2),
        "exponential":  dict(dash="dash",     width=2),
        "logarithmic":  dict(dash="dashdot",  width=2),
        "random_forest":dict(dash="longdash", width=2),
        "lowess":       dict(dash="solid",    width=2),
        "fallback":     dict(dash="dot",      width=2),
    }

    for c in countries:
        df_c = processed_data[
            (processed_data["country"] == c)
        ].dropna(subset=[x_attr, y_attr])

        # If we're predicting over time, restrict training data to selected years
        if x_attr == "year":
            real_year_max = processed_data["year"].max()
            fit_start = year_range[0]
            fit_end = min(year_range[1], real_year_max)

            df_c = df_c[(df_c["year"] >= fit_start) & (df_c["year"] <= fit_end)]

        if len(df_c) < 2:
            continue

        x = df_c[x_attr].values.reshape(-1, 1)
        y = df_c[y_attr].values

        style = base_styles.get(model_type, base_styles["fallback"]).copy()
        base_color = _get_country_color(fig, c)
        if base_color is not None:
            style["color"] = base_color

        if model_type == "polynomial":
            if poly_degree is None:
                degree = 1
            else:
                try:
                    degree = int(poly_degree)
                except (TypeError, ValueError):
                    degree = 1

            if degree < 1:
                degree = 1
            max_degree_data = max(1, len(np.unique(x)) - 1)
            max_degree_hard = 8
            degree = min(degree, max_degree_data, max_degree_hard)

            y_pred = _fit_polynomial(x, y, x_pred, degree)
            line_label = f"{c} Polynomial (deg={degree})"

        elif model_type == "exponential":
            mask = y > 0
            if mask.sum() < 2:
                continue
            x_fit = x[mask]
            y_fit = np.log(y[mask])
            model = LinearRegression().fit(x_fit, y_fit)
            log_y_pred = model.predict(x_pred)
            y_pred = np.exp(log_y_pred)
            line_label = f"{c} Exponential"

        elif model_type == "logarithmic":
            mask = x.flatten() > 0
            if mask.sum() < 2:
                continue
            x_fit = np.log(x[mask])
            y_fit = y[mask]
            model = LinearRegression().fit(x_fit, y_fit)
            x_pred_log = np.log(x_pred)
            y_pred = model.predict(x_pred_log)
            line_label = f"{c} Logarithmic"

        elif model_type == "random_forest":
            model = RandomForestRegressor(
                n_estimators=200,
                random_state=0,
            )
            model.fit(x, y)
            y_pred = model.predict(x_pred)
            line_label = f"{c} Random Forest"

        elif model_type == "lowess":
            if not _HAS_LOWESS:
                continue

            x_flat = x.flatten()
            smoothed = lowess(y, x_flat, frac=0.3, return_sorted=True)

            lowess_start = max(year_start, real_year_min)
            lowess_end = min(year_end, real_year_max)

            mask = (smoothed[:, 0] >= lowess_start) & (smoothed[:, 0] <= lowess_end)
            if mask.sum() < 2:
                continue

            x_lowess = smoothed[mask, 0]
            y_lowess = smoothed[mask, 1]

            fig.add_trace(
                go.Scatter(
                    x=x_lowess,
                    y=y_lowess,
                    mode="lines",
                    name=f"{c} LOWESS",
                    line=style,
                )
            )
            continue

        else:
            y_pred = _fit_polynomial(x, y, x_pred, degree=1)
            line_label = f"{c} Linear"

        fig.add_trace(
            go.Scatter(
                x=x_pred.flatten(),
                y=y_pred,
                mode="lines",
                name=line_label,
                line=style,
            )
        )

    return fig
