from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

co2 = pd.read_csv('data/owid-co2-data.csv')
fuel_consumption_by_fuel_type = pd.read_csv('data/fossil-fuel-consumption-by-fuel-type/fossil-fuel-consumption-by-fuel-type.csv')
fuel_price_index = pd.read_csv('data/fossil-fuel-price-index/fossil-fuel-price-index.csv')
fuel_production = pd.read_csv('data/fossil-fuel-production/fossil-fuel-production.csv')

co2.info()
fuel_consumption_by_fuel_type.info()
fuel_price_index.info()
fuel_production.info()

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)
