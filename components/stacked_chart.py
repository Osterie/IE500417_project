from dash import html, dcc, Output, Input, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd


def create_stacked_chart_layout(processed_data):
    invalid = {"year", "country"}
    attr_options = [
        c for c in processed_data.columns
        if c not in invalid
    ]

    return html.Div(
        id="stacked-chart-container",
        children=[
            html.H2("Stacked Summary for Selected Countries & Time Range", style={"textAlign": "center"}),

            html.Label("Stacked attributes (auto-adds main Y):"),
            dcc.Dropdown(
                id="stacked-attr-selection",
                options=[{"label": a, "value": a} for a in attr_options],
                value=[], 
                multi=True,
                placeholder="Pick one or more attributes...",
                style={"width": "450px", "marginBottom": "15px"},
            ),

            dcc.Graph(id="stacked-chart-graph"),
        ],
    )


def register_stacked_chart_callbacks(processed_data):

    INVALID = {"year", "country"}

    @callback(
        Output("stacked-attr-selection", "value"),
        Output("stacked-chart-graph", "figure"),
        Input("dropdown-selection", "value"),
        Input("year-range-slider", "value"),
        Input("dropdown-selection-y", "value"),
        Input("stacked-attr-selection", "value"),
    )
    def update_stacked_attrs_and_graph(countries, year_range, main_y, selected_attrs):
        if not countries or not year_range:
            raise PreventUpdate

        if isinstance(countries, str):
            countries = [countries]

        selected_attrs = selected_attrs or []

        # Always remove invalids if they got in
        selected_attrs = [a for a in selected_attrs if a not in INVALID]

        auto_add_allowed = bool(main_y) and main_y not in INVALID
        if auto_add_allowed and main_y not in selected_attrs:
            selected_attrs = selected_attrs + [main_y]

        if not selected_attrs:
            fig = px.bar(title="Select one or more attributes to build a stacked summary.")
            fig.update_layout(template="plotly_white")
            return selected_attrs, fig

        start, end = year_range

        dff = processed_data[
            (processed_data["country"].isin(countries)) &
            (processed_data["year"] >= start) &
            (processed_data["year"] <= end)
        ].copy()

        if dff.empty:
            fig = px.bar(title="No data available for selected countries and year range.")
            fig.update_layout(template="plotly_white")
            return selected_attrs, fig

        for col in selected_attrs:
            dff[col] = pd.to_numeric(dff[col], errors="coerce")

        dff = dff.dropna(subset=selected_attrs, how="all")
        if dff.empty:
            fig = px.bar(title="No numeric data available for selected attributes in this range.")
            fig.update_layout(template="plotly_white")
            return selected_attrs, fig

        agg = (
            dff.groupby("country")[selected_attrs]
            .sum()
            .reset_index()
        )

        long_df = agg.melt(
            id_vars="country",
            value_vars=selected_attrs,
            var_name="attribute",
            value_name="total",
        )

        order = (
            agg.assign(_total=agg[selected_attrs].sum(axis=1))
               .sort_values("_total", ascending=False)["country"]
               .tolist()
        )

        fig = px.bar(
            long_df,
            x="country",
            y="total",
            color="attribute",
            barmode="stack",
            category_orders={"country": order},
            title=f"Stacked totals ({start}–{end})",
            labels={"total": "Total over selected range", "attribute": "Attribute"},
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Country",
            yaxis_title="Total over period",
        )

        return selected_attrs, fig