from dash import Dash, html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
from data_reading import preprocess_data

processed_data = pd.DataFrame()
try:
    processed_data =  pd.read_csv('data/processed_data.csv')
except FileNotFoundError:
    processed_data = preprocess_data()
    processed_data.to_csv('data/processed_data.csv', index=False)

app = Dash()

app.layout = html.Div(
    id="main-container",
    children=[
        html.H1("Data Visualization", style={"textAlign":"center"}),

        html.Div(
            className="control-grid",
            children=[
                html.Div([
                    html.Label("Select a country/region:"),
                    dcc.Dropdown(processed_data.country.unique(),
                                 'Canada',
                                 id='dropdown-selection',
                                 multi=True)
                ]),
                html.Div([
                    html.Label("X-axis attribute:"),
                    dcc.Dropdown(processed_data.columns.values,
                                 'year',
                                 id='dropdown-selection-x')
                ]),
                html.Div([
                    html.Label("Y-axis attribute:"),
                    dcc.Dropdown(processed_data.columns.values,
                                 'co2',
                                 id='dropdown-selection-y')
                ])
            ]
        ),

        html.Div(
            className="graph-card",
            children=[
                dcc.Graph(id='graph-content')
            ]
        )
    ]
)

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('dropdown-selection-x', 'value'),
    Input('dropdown-selection-y', 'value'),
)
def update_graph(country, x_attr, y_attr):
    if (country is None) or (x_attr is None) or (y_attr is None):
        raise PreventUpdate

    if isinstance(country, str):
        countries = [country]
    else:
        countries = country

    dff = processed_data[processed_data.country.isin(countries)]

    if x_attr == "year":
        fig = px.line(dff, x=x_attr, y=y_attr, color="country")
    else:
        fig = px.scatter(dff, x=x_attr, y=y_attr, color="country")


    fig.update_layout(
        template="plotly_white",
        title=f"{y_attr} vs {x_attr}",
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig



if __name__ == '__main__':
    app.run(debug=True)
