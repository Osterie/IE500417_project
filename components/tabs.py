from dash import dcc, html
from components.stacked_chart import create_stacked_chart_layout
from components.layout import create_layout



def create_tabs_layout(processed_data):
    """Returns the layout section for the tabs component."""
    return html.Div([
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                dcc.Tab(
                    label="Main Visualization",
                    value="tab-1",
                    children=create_layout(processed_data)
                ),
                dcc.Tab(
                    label="Stacked Chart",
                    value="tab-2",
                    children=create_stacked_chart_layout()
                ),
            ]
        )
    ])