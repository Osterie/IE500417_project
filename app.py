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

processed_data.info()

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(processed_data.country.unique(), 'Canada', id='dropdown-selection', multi=True),
    dcc.Dropdown(processed_data.columns.values, 'year', id='dropdown-selection-x'),
    dcc.Dropdown(processed_data.columns.values, 'co2', id='dropdown-selection-y'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('dropdown-selection-x', 'value'),
    Input('dropdown-selection-y', 'value'),
)
def update_graph(country, x_attr, y_attr):
    if (country is None) or (x_attr is None) or (y_attr is None):
        raise PreventUpdate
    print(country, x_attr, y_attr)
    dff = processed_data[processed_data.country==country]
    

    if x_attr == 'year':
        fig = px.line(dff, x=x_attr, y=y_attr, color='country')
    else:
        fig = px.scatter(dff, x=x_attr, y=y_attr, color='country')

    return fig



if __name__ == '__main__':
    app.run(debug=True)
