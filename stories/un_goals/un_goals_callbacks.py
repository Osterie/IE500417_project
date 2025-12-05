from dash import callback, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from stories.un_goals.un_goals import UN_GOALS
from util import (
    assign_new_color,
    create_line_chart,
    get_data_for_countries,
    get_data_in_year_range,
    extract_existing_colors,
    do_rolling_average,
    do_prediction,
    
)



def register_un_story_callbacks(processed_data):

    def apply_country_colors_and_sort(fig):
        fig = go.Figure(fig)

        traces = list(fig.data)

        def parse_key(tr):
            name = getattr(tr, "name", "") or ""
            country = name.split()[0] if name else ""
            return (country, name)

        traces_sorted = sorted(traces, key=parse_key)
        fig.data = tuple(traces_sorted)

        # Apply consistent colors
        for tr in fig.data:
            name = getattr(tr, "name", None)
            if not name:
                continue
            country = name.split()[0]

        return fig

    def enforce_nonnegative_y(fig):
        fig = go.Figure(fig)

        max_y = None
        for tr in fig.data:
            y = getattr(tr, "y", None)
            if y is None:
                continue
            for v in y:
                try:
                    val = float(v)
                except (TypeError, ValueError):
                    continue
                if max_y is None or val > max_y:
                    max_y = val

        if max_y is None:
            fig.update_yaxes(range=[0, 1])
        else:
            fig.update_yaxes(range=[0, max_y * 1.05])

        return fig

    def add_un_markers(fig, prediction_mode):
        fig = go.Figure(fig)

        prediction_on = bool(prediction_mode and "predict" in prediction_mode)

        markers = [
            (UN_GOALS["Rio_earth_summit"], "Rio Earth Summit", False),
            (UN_GOALS["paris_agreement_year"], "Paris Agreement", False),
            (UN_GOALS["cut_ghg_by_43%"], "cut ghg by 43%", False),
            (UN_GOALS["net_zero_year"], "Net-zero 2050", True),
        ]

        for year, label, only_with_prediction in markers:
            if only_with_prediction and not prediction_on:
                continue

            fig.add_vline(
                x=year,
                line_dash="dot",
                line_color="grey",
                line_width=1,
                opacity=0.6,
            )
            fig.add_annotation(
                x=year,
                y=1,
                xref="x",
                yref="paper",
                text=label,
                showarrow=False,
                yanchor="bottom",
                textangle=-90,
                font=dict(size=10, color="grey"),
            )

        return fig

    

    # Main Graph

    @callback(
        Output("un-graph-content", "figure"),
        Output("un-goals-indicator", "children"),
        Input("un-dropdown-selection", "value"),
        Input("un-year-range-slider", "value"),
        Input("un-show-rolling-average", "value"),
        Input("un-rolling-window-size", "value"),
        Input("un-enable-prediction", "value"),
        Input("un-model-selection", "value"),
        Input("un-polynomial-degree", "value"),
        State("un-graph-content", "figure")
    )
    def update_un_graph(
        countries,
        year_range,
        show_rolling,
        rolling_window,
        prediction_mode,
        model_selection,
        poly_degree,
        existing_figure
    ):
        # Fixed axes for this story
        x_attr = "year"
        y_attr = "total_ghg - Mt"

        if (countries is None) or (year_range is None):
            raise PreventUpdate

        if isinstance(countries, str):
            countries = [countries]

        dff = get_data_for_countries(processed_data, countries)
        if dff.empty:
            raise PreventUpdate

        dff = get_data_in_year_range(dff, year_range)
        if dff.empty:
            raise PreventUpdate

        existing_color_map = extract_existing_colors(existing_figure) if existing_figure else {}
        final_color_map = dict(existing_color_map)

        for country in countries:
            if country not in final_color_map:
                final_color_map[country] = assign_new_color(final_color_map)


        fig = create_line_chart(dff, x_attr, y_attr, color_map=final_color_map)


        fig = do_rolling_average(
            show_rolling,
            rolling_window,
            countries,
            dff,
            fig,
            y_attr,
        )

        fig = do_prediction(
            prediction_mode,
            model_selection,
            processed_data,
            countries,
            x_attr,
            y_attr,
            year_range,
            poly_degree,
            fig,
        )

        fig = add_un_markers(fig, prediction_mode)

        fig.update_layout(
            template="plotly_white",
            title=f"{y_attr} vs {x_attr} (UN goals context)",
            title_x=0.5,
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(
                orientation="v",
                x=1.02,
                xanchor="left",
                y=1,
                yanchor="top",
            ),
        )

        fig = enforce_nonnegative_y(fig)

        year_start, year_end = year_range
        rio_summit = UN_GOALS["Rio_earth_summit"]
        paris_year = UN_GOALS["paris_agreement_year"]
        half_goal = UN_GOALS["cut_ghg_by_43%"]
        net_zero_year = UN_GOALS["net_zero_year"]
        years_left = net_zero_year - year_end

        indicator_text = (
            f"Rio Earth Summit in {rio_summit}, Paris Agreement in {paris_year}, goal to cut by 43% in {half_goal}, and net-zero around {net_zero_year}. "
            f"This view covers {year_start}–{year_end}; there are {years_left} years left to 2050."
        )

        return fig, indicator_text

    # Prediction and slider

    @callback(
        Output("un-model-selection-container", "style"),
        Output("un-year-range-slider", "max", allow_duplicate=True),
        Output("un-year-range-slider", "value", allow_duplicate=True),
        Input("un-enable-prediction", "value"),
        State("un-year-range-slider", "value"),
        prevent_initial_call="initial_duplicate",
    )
    def toggle_un_prediction_mode(prediction_mode, current_range):
        year_min = processed_data["year"].min()
        year_max = processed_data["year"].max()
        extend_year_max = year_max + 50

        if current_range is None:
            current_range = [year_min, year_max]

        if prediction_mode and "predict" in prediction_mode:
            new_max = extend_year_max
            new_range = [year_min, 2050]
            return {"display": "block"}, new_max, new_range
        else:
            new_max = year_max
            new_range = [
                max(current_range[0], year_min),
                min(current_range[1], new_max),
            ]
            return {"display": "none"}, new_max, new_range


    @callback(
    Output("un-polynomial-degree-container", "style"),
    Input("un-model-selection", "value"),
    Input("un-enable-prediction", "value"),
    )
    def toggle_un_polynomial_degree(model_selection, prediction_mode):
        if not (prediction_mode and "predict" in prediction_mode):
            return {"display": "none", "marginTop": "10px"}

        if not model_selection:
            return {"display": "none", "marginTop": "10px"}

        selected = model_selection if isinstance(model_selection, list) else [model_selection]

        if "polynomial" in selected:
            return {"display": "block", "marginTop": "10px"}

        return {"display": "none", "marginTop": "10px"}


    
    # Poduction and consumption graphs

    @callback(
        Output("un-prod-graph", "figure"),
        Output("un-cons-graph", "figure"),
        Input("un-dropdown-selection", "value"),
        Input("un-year-range-slider", "value"),
        Input("un-show-rolling-average", "value"),
        Input("un-rolling-window-size", "value"),
        Input("un-enable-prediction", "value"),
        Input("un-model-selection", "value"),
        Input("un-polynomial-degree", "value"),
        State("un-graph-content", "figure"),
    )
    def update_prod_cons_graphs(
        countries,
        year_range,
        show_rolling,
        rolling_window,
        prediction_mode,
        model_selection,
        poly_degree,
        graph_content
    ):
        if countries is None or year_range is None:
            raise PreventUpdate

        if isinstance(countries, str):
            countries = [countries]

        existing_color_map = extract_existing_colors(graph_content) if graph_content else {}
        final_color_map = dict(existing_color_map)

        for country in countries:
            if country not in final_color_map:
                final_color_map[country] = assign_new_color(final_color_map)

        year_start, year_end = year_range

        dff = processed_data[processed_data["country"].isin(countries)].copy()
        dff = dff[(dff["year"] >= year_start) & (dff["year"] <= year_end)]
        if dff.empty:
            raise PreventUpdate

        oil_prod_col = "oil production - TWh"
        gas_prod_col = "gas production - TWh"
        oil_cons_col = "oil consumption - TWh"
        gas_cons_col = "gas consumption - TWh"

        # Production 
        prod_fig = go.Figure()

        for country in countries:
            df_c = dff[dff["country"] == country].sort_values("year")

            color = final_color_map.get(country)

            df_oil = df_c.dropna(subset=[oil_prod_col])
            if not df_oil.empty:
                prod_fig.add_trace(
                    go.Scatter(
                        x=df_oil["year"],
                        y=df_oil[oil_prod_col],
                        mode="lines",
                        name=f"{country} oil production",
                        legendgroup=country,
                        line=dict(color=color) if color else None,
                    )
                )

            df_gas = df_c.dropna(subset=[gas_prod_col])
            if not df_gas.empty:
                prod_fig.add_trace(
                    go.Scatter(
                        x=df_gas["year"],
                        y=df_gas[gas_prod_col],
                        mode="lines",
                        name=f"{country} gas production",
                        legendgroup=country,
                        line=dict(dash="dash", color=color) if color else dict(dash="dash"),
                    )
                )

        # Rolling average for production
        prod_fig = do_rolling_average(
            show_rolling,
            rolling_window,
            countries,
            dff,
            prod_fig,
            oil_prod_col,
        )
        prod_fig = do_rolling_average(
            show_rolling,
            rolling_window,
            countries,
            dff,
            prod_fig,
            gas_prod_col,
        )

        # Prediction for production
        if prediction_mode and "predict" in prediction_mode:
            x_attr = "year"
            for y_attr in [oil_prod_col, gas_prod_col]:
                prod_fig = do_prediction(
                    prediction_mode,
                    model_selection,
                    processed_data,
                    countries,
                    x_attr,
                    y_attr,
                    year_range,
                    poly_degree,
                    prod_fig,
                )

        prod_fig = add_un_markers(prod_fig, prediction_mode)

        prod_fig.update_layout(
            template="plotly_white",
            title="Oil and gas production over time",
            xaxis_title="Year",
            yaxis_title="Production (TWh)",
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(
                orientation="v",
                x=1.02,
                xanchor="left",
                y=1,
                yanchor="top",
            ),
        )

        prod_fig = enforce_nonnegative_y(prod_fig)

        # Consumption 
        cons_fig = go.Figure()

        for country in countries:
            df_c = dff[dff["country"] == country].sort_values("year")

            color = final_color_map.get(country)

            df_oil = df_c.dropna(subset=[oil_cons_col])
            if not df_oil.empty:
                cons_fig.add_trace(
                    go.Scatter(
                        x=df_oil["year"],
                        y=df_oil[oil_cons_col],
                        mode="lines",
                        name=f"{country} oil consumption",
                        legendgroup=country,
                        line=dict(color=color)
                    )
                )

            df_gas = df_c.dropna(subset=[gas_cons_col])
            if not df_gas.empty:
                cons_fig.add_trace(
                    go.Scatter(
                        x=df_gas["year"],
                        y=df_gas[gas_cons_col],
                        mode="lines",
                        name=f"{country} gas consumption",
                        legendgroup=country,
                        line=dict(dash="dash", color=color) if color else dict(dash="dash"),
                    )
                )

        # Rolling average for consumption
        cons_fig = do_rolling_average(
            show_rolling,
            rolling_window,
            countries,
            dff,
            cons_fig,
            oil_cons_col,
        )
        cons_fig = do_rolling_average(
            show_rolling,
            rolling_window,
            countries,
            dff,
            cons_fig,
            gas_cons_col,
        )

        # Prediction for consumption
        if prediction_mode and "predict" in prediction_mode:
            x_attr = "year"
            for y_attr in [oil_cons_col, gas_cons_col]:
                cons_fig = do_prediction(
                    prediction_mode,
                    model_selection,
                    processed_data,
                    countries,
                    x_attr,
                    y_attr,
                    year_range,
                    poly_degree,
                    cons_fig,
                )

        cons_fig = add_un_markers(cons_fig, prediction_mode)

        cons_fig.update_layout(
            template="plotly_white",
            title="Oil and gas consumption over time",
            xaxis_title="Year",
            yaxis_title="Consumption (TWh)",
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(
                orientation="v",
                x=1.02,
                xanchor="left",
                y=1,
                yanchor="top",
            ),
        )

        cons_fig = enforce_nonnegative_y(cons_fig)

        return prod_fig, cons_fig
