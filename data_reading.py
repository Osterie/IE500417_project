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

# co2 = pd.read_csv('data/owid-co2-data.csv')
# fuel_consumption_by_fuel_type = pd.read_csv('data/fossil-fuel-consumption-by-fuel-type/fossil-fuel-consumption-by-fuel-type.csv')
# fuel_production = pd.read_csv('data/fossil-fuel-production/fossil-fuel-production.csv')
# fuel_price_index = pd.read_csv('data/fossil-fuel-price-index/fossil-fuel-price-index.csv')

# co2 = co2[co2.columns.intersection(attributes_we_care_about)]
# fuel_consumption_by_fuel_type= fuel_consumption_by_fuel_type[fuel_consumption_by_fuel_type.columns.intersection(attributes_we_care_about)]
# fuel_production= fuel_production[fuel_production.columns.intersection(attributes_we_care_about)]
# fuel_price_index= fuel_price_index[fuel_price_index.columns.intersection(attributes_we_care_about)]


def preprocess_data():
    
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
    
    co2 = read_data('data/owid-co2-data.csv', attributes_we_care_about)
    fuel_consumption_by_fuel_type = read_data('data/fossil-fuel-consumption-by-fuel-type/fossil-fuel-consumption-by-fuel-type.csv', attributes_we_care_about)
    fuel_production = read_data('data/fossil-fuel-production/fossil-fuel-production.csv', attributes_we_care_about)
    fuel_price_index = read_data('data/fossil-fuel-price-index/fossil-fuel-price-index.csv', attributes_we_care_about)

    # Only use countries common in all datasets.
    common_countries = set(co2['country']).intersection(
        set(fuel_consumption_by_fuel_type['country']),
        set(fuel_production['country'])
    )
    
    final_dataframe = pd.DataFrame(columns=attributes_we_care_about)

    
    for country in list(common_countries):
        co2_years_for_country = set(co2[co2['country'] == country]['year'])
        fuel_consumption_by_fuel_type_years_for_country = set(fuel_consumption_by_fuel_type[fuel_consumption_by_fuel_type['country'] == country]['year'])
        fuel_production_years_for_country = set(fuel_production[fuel_production['country'] == country]['year'])

        common_years = co2_years_for_country.intersection(
            fuel_consumption_by_fuel_type_years_for_country,
            fuel_production_years_for_country
        )

        co2_data = co2[(co2['country'] == country) & (co2['year'].isin(common_years))]
        consumption = fuel_consumption_by_fuel_type[
            (fuel_consumption_by_fuel_type['country'] == country) &
            (fuel_consumption_by_fuel_type['year'].isin(common_years))
        ]
        production = fuel_production[
            (fuel_production['country'] == country) &
            (fuel_production['year'].isin(common_years))
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



def read_data(path, relevant_attributes = []):
    
    data = pd.read_csv(path)
    if (relevant_attributes != []):
        data = data[data.columns.intersection(relevant_attributes)]

    return data



# co2 = pd.read_csv('data/owid-co2-data.csv')
# fuel_consumption_by_fuel_type = pd.read_csv('data/fossil-fuel-consumption-by-fuel-type/fossil-fuel-consumption-by-fuel-type.csv')
# fuel_production = pd.read_csv('data/fossil-fuel-production/fossil-fuel-production.csv')
# fuel_price_index = pd.read_csv('data/fossil-fuel-price-index/fossil-fuel-price-index.csv')

# co2 = co2[co2.columns.intersection(attributes_we_care_about)]
# fuel_consumption_by_fuel_type= fuel_consumption_by_fuel_type[fuel_consumption_by_fuel_type.columns.intersection(attributes_we_care_about)]
# fuel_production= fuel_production[fuel_production.columns.intersection(attributes_we_care_about)]
# fuel_price_index= fuel_price_index[fuel_price_index.columns.intersection(attributes_we_care_about)]