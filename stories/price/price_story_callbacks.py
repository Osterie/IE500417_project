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

    # @callback(
    #     Output('price-selected-story-mode', 'children'),
    #     Output('price-selected-story-description', 'children'),
    #     Input("price-story-selector", "value")
    # )
    # def update_story_mode_label(selected_story_mode):
    #     if selected_story_mode == "Self-Exploration":
    #         story_mode_explanation = "You have chosen the story mode: Self-Exploration. Enjoy exploring the data on your own!"
    #         story_mode_description = "For this exploration mode there is no predefined story. Feel free to select different countries, attributes, wars and time ranges to discover insights on your own."
    #         return story_mode_explanation, story_mode_description
    #     elif selected_story_mode == "Global Conflicts":
    #         story_mode_explanation = "You have chosen the story mode: Global Conflicts. Explore the impact of global conflicts on the oil and gas industry."
    #         story_mode_description = "As you can see on the graph, there is a large dip in the worlds oil production when the Soviet-Afghan price and Iran-Iraq price started, around 1979. Interestingly we do not see a notable dip in oil production during any of the other wars we have included. Infact, during the period of the Vitenam price (from when USA got involved), we see a huge increase in oil production globally. This could be due to various factors such as increased demand for oil to support the price effort, or perhaps other geopolitical factors at play during that time. We can see that in 1965, at the start of USA's involvement in the price, the global production of oil was around 18 000 TWh, whilst 10 years later, in 1975, the production price around 32 000 TWh. This is about a 78% increase in production over a decade."
    #         return story_mode_explanation, story_mode_description
    #     elif selected_story_mode == "Iraq Wars":
    #         story_mode_explanation = "You have chosen the story mode: Iraq Wars. Analyze the effects of the wars in Iraq on its oil and gas industry."
    #         story_mode_description = "We can observe significant decreases in Iraq's oil production during the periods of the Iran-Iraq War and Gulf War, and also a clear dip the year the Iraq War 2003 started. Interestingly we also see that the years leading up to the wars show an increase in production, possibly indicating efforts to maximize output before the anticipated conflicts. Overall, these wars had a profound impact on Iraq's oil production."
    #         story_mode_description += "\n"
    #         story_mode_description += "We can also observe that oil production steadily increases during each price, and that after the price ends, production quickly recovers and continues to grow. This could indicate that the oil infrastructure was not heavily damaged during these conflicts, or that there were rapid reconstruction efforts post-price to restore production levels, perhaps since oil is such a crucial part of Iraq's economy."
    #         return story_mode_explanation, story_mode_description
    #     else:
    #         return "Unknown Mode", ""
        
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
                # ["Germany", "Italy", "Spain"],
                ["Germany", "Italy", "Russia", "United Kingdom"],
                "Oil Price ($)",
                "co2 - Mt",
            )
            
        elif selected_story_mode == "Gas dependent countries":
            return (
                ["Germany", "United Kingdom", "Italy", "Ukraine"],
                # ["Germany", "Italy", "United Kingdom", "Netherlands"],
                "Oil Price ($)",
                "co2 - Mt",
            )

        elif selected_story_mode == "Oil producing countries":
            return (
                ["Russia", "Norway", "United Kingdom", "Romania"],
                "Oil Price ($)",
                "co2 - Mt",
            )
        elif selected_story_mode == "Gas producing countries":
            return (
                ["Norway", "United Kingdom", "Romania", "Ukraine"],
                "Oil Price ($)",
                "co2 - Mt",
            )

        raise PreventUpdate