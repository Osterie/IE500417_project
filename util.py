
import plotly.express as px
from components.prediction.callbacks_prediction import add_prediction



def _get_country_color(fig, country_name):
    for tr in fig.data:
        if tr.name == country_name:
            line = getattr(tr, "line", None)
            if line and getattr(line, "color", None) is not None:
                return line.color
    return None

def create_line_chart_old(dff, x_attr, y_attr):
    fig = px.line(dff, x=x_attr, y=y_attr, color="country")
    return fig

def create_line_chart(dff, x_attr, y_attr, color_map):
    fig = px.line(
        dff,
        x=x_attr,
        y=y_attr,
        color="country",
        color_discrete_map=color_map
    )
    return fig


def create_scatter_chart(dff, x_attr, y_attr):
    fig = px.scatter(dff, x=x_attr, y=y_attr, color="country")
    return fig

def create_scatter_chart(dff, x_attr, y_attr, color_map):
    fig = px.scatter(
        dff,
        x=x_attr,
        y=y_attr,
        color="country",
        color_discrete_map=color_map
    )
    return fig

def get_data_for_countries(processed_data, countries):
    if isinstance(countries, str):
        countries = [countries]
    return processed_data[processed_data.country.isin(countries)]

def get_data_in_year_range(processed_data, year_range):
    return processed_data[
        (processed_data['year'] >= year_range[0]) &
        (processed_data['year'] <= year_range[1])
    ]


def do_rolling_average(show_rolling, rolling_window, countries, dff, fig, y_attr):
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
    return fig

def do_prediction(prediction_mode, model_selection, processed_data, countries, x_attr, y_attr, year_range, poly_degree, fig, color_map=None, ):
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
                color_map=color_map,
            )
    return fig



def extract_existing_colors(existing_figure):
    if existing_figure is None or "data" not in existing_figure:
        return {}

    mapping = {}
    for trace in existing_figure["data"]:
        name = trace.get("name")
        color = trace.get("line", {}).get("color") or trace.get("marker", {}).get("color")
        if name and color:
            mapping[name] = color
    return mapping


def assign_new_color(existing_colors):
    palette = px.colors.qualitative.Plotly
    for color in palette:
        if color not in existing_colors.values():
            return color
    return palette[len(existing_colors) % len(palette)]
