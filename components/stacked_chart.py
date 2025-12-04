from dash import html, dcc, Output, Input, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd


def create_stacked_chart_layout():
    """Returns the layout section for the stacked chart component.
    This includes a dropdown to choose which dataset to visualize
    and a graph to display the stacked chart.
    """

    return html.Div(
        id="stacked-chart-container",
        children=[
            html.H2("Oil & Gas Stacked Bar Chart", style={'textAlign':'center'}),

            html.Div("Select Dataset:"),
            dcc.Dropdown(
                id="stacked-chart-dropdown",
                options=[
                    {"label": "Oil and Gas Production", "value": "oil_gas_production"},
                    {"label": "Oil and Gas Emissions", "value": "oil_gas_emissions"},
                    {"label": "Oil and Gas Consumption", "value": "oil_gas_consumption"},

                ],
                value="oil_gas_production", # default value
                clearable=False,
                style={"width": "300px", "marginBottom": "20px"},
            ),
            dcc.Graph(id="stacked-chart-graph"),

            html.Div(
                children=[
                    html.Label("Select Year:"),
                    dcc.Slider(
                        id="stacked-chart-year-slider",
                        min=1965,
                        max=2023,
                        value=2023,
                        marks={str(year): str(year) for year in range(1965, 2023, 5)},
                        step=1,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ]
            )
        ]
    )
    


# Callback to update the stacked chart based on graph and slider inputs.    

def register_stacked_chart_callbacks(app, processed_data):
    # We first update the slider range based on the selected dataset
    @app.callback(
        Output("stacked-chart-year-slider", "min"),
        Output("stacked-chart-year-slider", "max"),
        Output("stacked-chart-year-slider", "value"),
        Output("stacked-chart-year-slider", "marks"),
        Input("stacked-chart-dropdown", "value"),
    )

    def update_stacked_chart_slider(selected_dataset):
        regions_data = ["North America", "Europe", "Asia", "Africa", "South America", "Oceania"]

        if selected_dataset is None:
            raise PreventUpdate
        
        data_filtered = processed_data[processed_data["country"].isin(regions_data)]

        # Find min and max years in the filtered data
        min_year = data_filtered["year"].min()
        max_year = data_filtered["year"].max()
        return min_year, max_year, max_year
    
    # Now we update the graph when the slider or dropdown changes
    @app.callback(
        Output("stacked-chart-graph", "figure"),
        Input("stacked-chart-dropdown", "value"),
        Input("stacked-chart-year-slider", "value"),
    )

    # Function to update the stacked chart graph based on the selected dataset and selected year
    def update_stacked_chart_graph(selected_dataset, selected_year):
        regions_data = ["North America", "Europe", "Asia", "Africa", "South America", "Oceania"]
        if selected_dataset is None or selected_year is None:
            raise PreventUpdate
        
        data_filtered = processed_data[
            (processed_data["country"].isin(regions_data)) &
            (processed_data["year"] == selected_year)
        ]

        if data_filtered.empty:
            return px.bar(title="No data available for the selected year and dataset.")
        

        if selected_dataset == "oil_gas_production":
            y_axis = ["oil production - TWh", "gas production - TWh"]
            title = f"Oil and Gas Production in {selected_year}"
            y_label = "Production (TWh)"


        elif selected_dataset == "oil_gas_emissions":
            y_axis = ["oil_co2", "gas_co2"]
            title = f"Oil and Gas CO2 Emissions in {selected_year}"
            y_label = "CO2 Emissions (MtCO2)"   



        elif selected_dataset == "oil_gas_consumption":
             y_axis = ["oil consumption - TWh", "gas consumption - TWh"]
             title = f"Oil and Gas Consumption in {selected_year}"
             y_label = "Consumption (TWh)"



        # Create the Grouped Bar Chart
        fig = px.bar(
            data_filtered,
            x="country",
            y=y_axis,
            title=title,
            labels={"value": y_label, "country": "Region", "variable": "Energy Source"},
            barmode="group",
        )
        fig.update_layout(xaxis_title="Region", yaxis_title=y_label)

        return fig
       
                 

    
        
    

  

             
                        







        
