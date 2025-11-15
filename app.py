from dash import Dash, html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd


attributes_we_care_about = [
    "year",
    "country",
    "oil production - TWh",
    "gas production - TWh",
    "oil consumption - TWh",
    "gas consumption - TWh",
    "co2",
    "gas_co2",
    "oil_co2",
    "population",
    "gdp",
    "co2_growth_abs",
    "co2_growth_prct",
    "co2_per_unit_energy",
    "total_ghg",
    "cumulative_oil_co2",
    "methane",
]

co2 = pd.read_csv('data/owid-co2-data.csv')
fuel_consumption_by_fuel_type = pd.read_csv('data/fossil-fuel-consumption-by-fuel-type/fossil-fuel-consumption-by-fuel-type.csv')
fuel_production = pd.read_csv('data/fossil-fuel-production/fossil-fuel-production.csv')
fuel_price_index = pd.read_csv('data/fossil-fuel-price-index/fossil-fuel-price-index.csv')

co2_relevant = co2[co2.columns.intersection(attributes_we_care_about)]
fuel_consumption_by_fuel_type_relevant= fuel_consumption_by_fuel_type[fuel_consumption_by_fuel_type.columns.intersection(attributes_we_care_about)]
fuel_production_relevant= fuel_production[fuel_production.columns.intersection(attributes_we_care_about)]
fuel_price_index_relevant= fuel_price_index[fuel_price_index.columns.intersection(attributes_we_care_about)]


def preprocess_data():

    # Only use countries common in all datasets.
    common_countries = set(co2_relevant['country']).intersection(
        set(fuel_consumption_by_fuel_type_relevant['country']),
        set(fuel_production_relevant['country'])
    )
    
    final_dataframe = pd.DataFrame(columns=attributes_we_care_about)

    
    for country in list(common_countries):
        co2_years_for_country = set(co2_relevant[co2_relevant['country'] == country]['year'])
        fuel_consumption_by_fuel_type_years_for_country = set(fuel_consumption_by_fuel_type_relevant[fuel_consumption_by_fuel_type_relevant['country'] == country]['year'])
        fuel_production_years_for_country = set(fuel_production_relevant[fuel_production_relevant['country'] == country]['year'])

        common_years = co2_years_for_country.intersection(
            fuel_consumption_by_fuel_type_years_for_country,
            fuel_production_years_for_country
        )

        co2_data = co2_relevant[(co2_relevant['country'] == country) & (co2_relevant['year'].isin(common_years))]
        consumption = fuel_consumption_by_fuel_type_relevant[
            (fuel_consumption_by_fuel_type_relevant['country'] == country) &
            (fuel_consumption_by_fuel_type_relevant['year'].isin(common_years))
        ]
        production = fuel_production_relevant[
            (fuel_production_relevant['country'] == country) &
            (fuel_production_relevant['year'].isin(common_years))
        ]


        dataframe = pd.DataFrame()
        dataframe = (
            co2_data
            .merge(consumption, on=['country', 'year'], how='inner')
            .merge(production, on=['country', 'year'], how='inner')
        )

        
        # print(dataframe)
        # print(dataframe.columns)
        # print('oil production - TWh' in dataframe.columns)
        
        # final_dataframe = pd.merge(final_dataframe, dataframe)
        final_dataframe = pd.merge(final_dataframe, dataframe, how='outer', on=attributes_we_care_about)
        
    return final_dataframe.sort_values(by=["country", "year"])



    # only use years which are common in all datasets.
    # Remove if not all datasets have data for same country.

    # Drop attributes we don't care about!

    # Combine into 1 fellse dataset

    # Attribtues we care about:


    # year
    # country / country
    # oil production - Twh
    # gas production - Twh
    # oil consumption - Twh
    # gas consumption - Twh
    # co2
    # gas_co2
    # oil_co2
    # population
    # gdp
    # co2_growth_abs - rename to co2 growth absolute?
    # co2_growth_prct - rename to co2 growth percent?
    # co2_per_unit_energy
    # total_ghg
    # cumulative_oil_co2
    # methane

    # maybe
    # gas_co2_per_capita
    # oil_co2_per_capita
    # cumulative_co2
    # cumulative_gas_co2
    # flaring_co2
    # cumulative_flaring_co2
    # energy_per_capita
    # energy_per_gdp
    # share_global_co2
    # share_global_cumulative_co2
    # share_global_cumulative_flaring_co2
    # share_global_cumulative_gas_co2
    # share_global_cumulative_oil_co2
    # share_global_flaring_co2
    # share_global_gas_co2
    # share_global_oil_co2
    # share_of_temperature_change_from_ghg
    # temperature_change_from_ch4
    # temperature_change_from_co2
    # temperature_change_from_ghg


print("starting")
processed_data = preprocess_data()

processed_data.to_csv('data/processed_data.csv', index=False)
print("done")

# co2.info()
# fuel_consumption_by_fuel_type.info()
# fuel_price_index.info()
# fuel_production.info()

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(processed_data.country.unique(), 'Canada', id='dropdown-selection', multi=True),
    dcc.Dropdown(processed_data.columns.values, 'year', id='dropdown-selection-x'),
    dcc.Dropdown(processed_data.columns.values, 'co2', id='dropdown-selection-y'),
    dcc.Graph(id='graph-content')
])

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value'),
#     # Input('dropdown-selection-x', 'x-attribute'),
#     # Input('dropdown-selection-y', 'y-attribute'),
# )
# def update_graph(value):
#     dff = processed_data[processed_data.country==value]
#     return px.line(dff, x='year', y='processed_data')
# def update_graph(country, x_attr, y_attr):
#     print(country, x_attr, y_attr)
#     dff = processed_data[processed_data.country==country]
#     return px.line(dff, x=x_attr, y=y_attr)


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
    return px.line(dff, x=x_attr, y=y_attr)



if __name__ == '__main__':
    app.run(debug=True)
