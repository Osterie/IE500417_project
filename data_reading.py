import pandas as pd

from file_paths import FilePaths

def preprocess_data():
    
    # Drop attributes we don't care about!
    attributes_we_care_about = get_attributes_we_care_about()
    
    co2 = read_data(FilePaths.CO2.value, attributes_we_care_about)
    fuel_consumption_by_fuel_type = read_data(FilePaths.FUEL_CONSUMPTION_BY_FUEL_TYPE.value, attributes_we_care_about)
    fuel_production = read_data(FilePaths.FUEL_PRODUCTION.value, attributes_we_care_about)
    fuel_price_index = read_data(FilePaths.FUEL_PRICE_INDEX.value, attributes_we_care_about)

    # Only use countries common in all datasets.
    common_countries = set(co2['country']).intersection(
        set(fuel_consumption_by_fuel_type['country']),
        set(fuel_production['country'])
    )
    
    final_dataframe = pd.DataFrame(columns=attributes_we_care_about)
    
    for country in list(common_countries):
        
        # only use years which are common in all datasets.
        # Remove if not all datasets have data for same country.
        common_years = get_common_years_between_dataframes_for_country(
            [co2, fuel_consumption_by_fuel_type, fuel_production],
            country
        )
        
        merged_data = merge_dataframes_by_common_country_and_years(
            [co2, fuel_consumption_by_fuel_type, fuel_production],
            country,
            common_years
        )
        
        final_dataframe = pd.merge(final_dataframe, 
            merged_data,
            how='outer', 
            on=attributes_we_care_about
        )

    final_dataframe = final_dataframe.sort_values(by=["country", "year"])
    
    final_dataframe = final_dataframe.rename(columns={
        'co2': 'co2 - Mt',
        'gas_co2': 'gas_co2 - Mt',
        'oil_co2': 'oil_co2 - Mt',
        'co2_growth_abs': 'co2_growth_abs - Mt',
        'co2_growth_prct': 'co2_growth_prct - %',
        'cumulative_oil_co2': 'cumulative_oil_co2 - Mt',
        'total_ghg': 'total_ghg - Mt'
    })

            
    return final_dataframe

def include_only_countries(data):
    data_with_codes = pd.read_csv(FilePaths.CO2.value)
    countries_without_codes = data_with_codes[data_with_codes['iso_code'].isnull()]['country'].unique()
    
    no_country_code = data[~data['country'].isin(countries_without_codes)].copy()
    return no_country_code

def read_data(path, relevant_attributes = []):
    data = pd.read_csv(path)
    if (relevant_attributes != []):
        data = data[data.columns.intersection(relevant_attributes)]

    return data

def get_common_years_between_dataframes_for_country(dataframes, country):
    
    all_years = []
    
    for dataframe in dataframes:
        if 'year' not in dataframe:
            raise ValueError("Dataframe does not contain 'year' column")
        if 'country' not in dataframe:
            raise ValueError("Dataframe does not contain 'country' column")
        years = set(dataframe[dataframe['country'] == country]['year'])
        all_years.append(years)

    common_years = set.intersection(*all_years)
    return common_years

def merge_dataframes_by_common_country_and_years(dataframes, country, common_years):
    
    attributes_we_care_about = get_attributes_we_care_about()
    final_dataframe = pd.DataFrame(columns=attributes_we_care_about)
    
    filtered_dataframes = []
    
    for dataframe in dataframes:
        if 'year' not in dataframe:
            raise ValueError("Dataframe does not contain 'year' column")
        if 'country' not in dataframe:
            raise ValueError("Dataframe does not contain 'country' column")
        
        filtered = dataframe[
            (dataframe['country'] == country) &
            (dataframe['year'].isin(common_years))
        ]
        
        filtered_dataframes.append(filtered)
        
    if not filtered_dataframes:
        return final_dataframe
    
    final_dataframe  = filtered_dataframes[0]
    
    for dataframe in filtered_dataframes[1:]:
        final_dataframe = final_dataframe.merge(dataframe, on=['country', 'year'], how='inner')

    return final_dataframe

def create_oil_gas_production_dataset(data):
    total_oil_gas_production = aggregate_total_oil_gas_production(data)
    total_oil_gas_production = total_oil_gas_production.sort_values(by='oil production - TWh (total)', ascending=False)
    return total_oil_gas_production

def aggregate_total_oil_gas_production(data):
    total_oil_production = (
        data.groupby('country')[['oil production - TWh', 'gas production - TWh']]
            .sum()
            .reset_index()
            .rename(columns={'oil production - TWh': 'oil production - TWh (total)', 
                             'gas production - TWh': 'gas production - TWh (total)'
            })
    )
    return total_oil_production

def create_oil_production_dataset_countries(total_oil_production, countries):
    total_oil_production_countries = total_oil_production[total_oil_production['country'].isin(countries)]
    total_oil_production_countries = total_oil_production_countries.sort_values(by='oil production - TWh (total)', ascending=False)
    return total_oil_production_countries

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
def get_attributes_we_care_about():
    return [
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