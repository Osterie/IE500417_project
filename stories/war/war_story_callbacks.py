from dash import callback, Input, Output, State
from stories.war.wars import wars
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from util import (
    create_line_chart,
    create_scatter_chart,
    get_data_for_countries,
    get_data_in_year_range,
    do_rolling_average,
    do_prediction,
)

def register_war_story_callbacks(processed_data):

    # @callback(
    #     Output("war-graph-content", "figure"),
    #     Input("war-selector", "value"),
    #     State("war-graph-content", "figure"),
    #     prevent_initial_call=True
    # )
    # def overlay_wars(selected_wars, base_figure):
    #     if not selected_wars:
    #         return base_figure

    #     fig = go.Figure(base_figure)

    #     for war_key in selected_wars:
    #         war = wars[war_key]
    #         fig.add_vrect(
    #             x0=war["start"],
    #             x1=war["end"],
    #             fillcolor="red",
    #             opacity=0.15,
    #             line_width=0,
    #             annotation_text=war["name"],
    #             annotation_position="top left"
    #         )

    #     return fig
    
    @callback(
        Output('war-graph-content', 'figure'),
        Input('war-dropdown-selection', 'value'),
        Input('war-dropdown-selection-x', 'value'),
        Input('war-dropdown-selection-y', 'value'),
        Input('war-year-range-slider', 'value'),
        Input('war-show-rolling-average', 'value'),
        Input('war-rolling-window-size', 'value'),
        Input('war-enable-prediction', 'value'),
        Input('war-model-selection', 'value'),
        Input('war-polynomial-degree', 'value'),
        Input("war-selector", "value"),
        prevent_initial_call=True,
    )
    def update_graph(countries, x_attr, y_attr, year_range, show_rolling, rolling_window, prediction_mode, model_selection, poly_degree, selected_wars):
        if (countries is None) or (x_attr is None) or (y_attr is None):
            raise PreventUpdate

        if isinstance(countries, str):
            countries = [countries]
            
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
            
        fig = add_wars(fig, selected_wars)

        fig.update_layout(
            template="plotly_white",
            title=f"{y_attr} vs {x_attr}",
            title_x=0.5,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        return fig

    def add_wars(fig, selected_wars):
        if not selected_wars:
            return fig

        fig = go.Figure(fig)

        for war_key in selected_wars:
            war = wars[war_key]
            fig.add_vrect(
                x0=war["start"],
                x1=war["end"],
                fillcolor="red",
                opacity=0.15,
                line_width=0,
                annotation_text=war["name"],
                annotation_position="top left"
            )

        return fig
    
    
    @callback(
        Output('war-slider-container', 'style'),
        Input('war-dropdown-selection-x', 'value')
    )
    def toggle_slider(x_attr):
        if x_attr == 'year':
            return {"display": "block"}
        else:
            return {"display": "none"}
        

    @callback(
        Output("war-model-selection-container", "style"),
        Output("war-year-range-slider", "max", allow_duplicate=True),
        Output("war-year-range-slider", "value", allow_duplicate=True),
        Input("war-enable-prediction", "value"),
        State("war-year-range-slider", "value"),
        prevent_initial_call="initial_duplicate",
    )
    def toggle_prediction_mode(prediction_mode, current_range):
        year_min = processed_data["year"].min()
        year_max = processed_data["year"].max()
        extend_year_max = year_max + 50

        if current_range is None:
            current_range = [year_min, year_max]

        if prediction_mode and "predict" in prediction_mode:
            new_max = extend_year_max
            new_range = [current_range[0], new_max]
            return {"display": "block"}, new_max, new_range
        else:
            new_max = year_max
            new_range = [
                max(current_range[0], year_min),
                min(current_range[1], new_max)
            ]
            return {"display": "none"}, new_max, new_range
