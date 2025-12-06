from dash import Input, Output, callback, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from components.prediction.callbacks_prediction import add_prediction
from util import (
    assign_new_color,
    create_scatter_chart,
    extract_existing_colors,
    get_data_for_countries,
    do_prediction,
)

def register_price_story_callbacks(processed_data):

    @callback(
        Output('price-graph-content', 'figure'),
        Input('price-dropdown-selection', 'value'),
        Input('price-dropdown-selection-x', 'value'),
        Input('price-dropdown-selection-y', 'value'),
        Input('price-enable-prediction', 'value'),
        Input('price-model-selection', 'value'),
        Input('price-polynomial-degree', 'value'),
        State('price-graph-content', 'figure'),
    )
    def update_graph(countries, x_attr, y_attr, prediction_mode, model_selection, poly_degree, existing_figure):
        if (countries is None) or (x_attr is None) or (y_attr is None):
            raise PreventUpdate

        if isinstance(countries, str):
            countries = [countries]
            
        dff = get_data_for_countries(processed_data, countries)
        
        existing_color_map = extract_existing_colors(existing_figure)

        final_color_map = {}
        
        for country in countries:
            if country in existing_color_map:
                final_color_map[country] = existing_color_map[country]
            else:
                final_color_map[country] = assign_new_color(existing_color_map)
            existing_color_map.update(final_color_map)
        
        
        effective_range = None

        fig = create_scatter_chart(dff, x_attr, y_attr, final_color_map)

        fig = do_prediction(
            prediction_mode,
            model_selection,
            processed_data,
            countries,
            x_attr,
            y_attr,
            effective_range,
            poly_degree,
            fig,
            final_color_map
        )
        
        fig.update_layout(
            template="plotly_white",
            title=f"{y_attr} vs {x_attr}",
            title_x=0.5,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        return fig

    @callback(
        Output("price-model-selection-container", "style"),
        Input("price-enable-prediction", "value"),
        prevent_initial_call="initial_duplicate",
    )
    def toggle_prediction_mode(prediction_mode):
        if prediction_mode and "predict" in prediction_mode:
            return {"display": "block"}
        else:
            return {"display": "none"}

    @callback(
        Output('price-selected-story-mode', 'children'),
        Output('price-selected-story-description', 'children'),
        Input("price-story-selector", "value")
    )
    def update_story_mode_label(selected_story_mode):
        story_mode_explanation = "Unknown Mode"
        story_mode_description = ""
        if selected_story_mode == "Oil dependent countries":
            story_mode_explanation = "You are viewing a story about some countries with high Oil consumption in Europe"
            story_mode_description = "We can see a sligth downwards trend for oil consumption for some oil dependent countries when the price of oil increases. This does intuitively make sense, although there are also many other factors affecting oil consumption."
        
        elif selected_story_mode == "Gas dependent countries":
            story_mode_explanation = "You are viewing a story about some countries with high Gas consumption in Europe"
            story_mode_description = "We excpected that when gass prices rose, the consumtion would also rise. This was not the case for every country, this could be because of external unknown causes. "
        
        elif selected_story_mode == "Oil producing countries":
            story_mode_explanation = "You are viewing a story about some countries with high Oil production in Europe"
            story_mode_description = "We can see that for the selected countries, oil production generaly rizes when oil prices raise. This can be because of when this or other countries need more oil, they are willing to pay more for it, also known as suply and demand."
        
        elif selected_story_mode == "Gas producing countries":
            story_mode_explanation = "You are viewing a story about some countries with high Oil consumption in Europe"
            story_mode_description = "We can see that for the selected countries, gass production generaly rizes or stays still when prices raises. This can be becuase of suply and demand, and for the countries that the price does not change, they might produce a set amount of gass per year."

        return story_mode_explanation, story_mode_description
        
    @callback(
        Output("price-dropdown-selection", "value", allow_duplicate=True),
        Output("price-dropdown-selection-x", "value", allow_duplicate=True),
        Output("price-dropdown-selection-y", "value", allow_duplicate=True),
        Input("price-story-selector", "value"),
        prevent_initial_call=True
    )
    def apply_story_mode_defaults(selected_story_mode):
        if selected_story_mode == "Oil dependent countries":
            return (
                ["Germany", "Italy", "United Kingdom"],
                "Oil Price ($)",
                "oil consumption - TWh",
            )
            
        elif selected_story_mode == "Gas dependent countries":
            return (
                ["Germany", "United Kingdom", "Italy", "Ukraine"],
                "Gas Price ($)",
                "gas consumption - TWh",
            )

        elif selected_story_mode == "Oil producing countries":
            return (
                ["Norway", "United Kingdom"],
                "Oil Price ($)",
                "oil production - TWh",
            )
        elif selected_story_mode == "Gas producing countries":
            return (
                ["Norway", "United Kingdom", "Romania", "Ukraine"],
                "Gas Price ($)",
                "gas production - TWh",
            )

        raise PreventUpdate