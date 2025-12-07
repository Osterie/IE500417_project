import pandas as pd
from data_reading import create_oil_production_dataset_countries, preprocess_data, include_only_countries
from data_reading import create_oil_gas_production_dataset, create_oil_gas_production_dataset2, create_oil_gas_consumption_dataset, create_oil_gas_consumption_dataset2


try:
    processed_data = pd.read_csv('data/processed_data.csv')
    processed_data_only_countries = pd.read_csv('data/processed_data_only_countries.csv')
except FileNotFoundError:
    processed_data = preprocess_data()
    processed_data_only_countries = include_only_countries(processed_data)
    processed_data_only_countries.to_csv('data/processed_data_only_countries.csv', index=False)
    processed_data.to_csv('data/processed_data.csv', index=False)

try:
    oil_production_data = pd.read_csv('data/total_oil_production.csv')
except FileNotFoundError:
    oil_production_data = create_oil_gas_production_dataset(processed_data)
    gas_production_data = create_oil_gas_production_dataset2(processed_data)
    oil_consumption_data = create_oil_gas_consumption_dataset(processed_data)
    gas_consumption_data = create_oil_gas_consumption_dataset2(processed_data)
    oil_production_data.to_csv('data/total_oil_production.csv', index=False)
    gas_production_data.to_csv('data/total_gas_production.csv', index=False)
    oil_consumption_data.to_csv('data/total_oil_consumption.csv', index=False)
    gas_consumption_data.to_csv('data/total_gas_consumption.csv', index=False)



# Iceland, Liechtenstein and Norway are in Europe but not in EU, are also part of EEA
countries_in_eu =[
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Republic of Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden"
]

countries_in_europe = [
"Albania",
"Andorra",
"Austria",
"Belarus",
"Belgium",
"Bosnia and Herzegovina",
"Bulgaria",
"Croatia",
"Denmark",
"Estonia",
"Finland",
"France",
"Germany",
"Greece",
"Hungary",
"Iceland",
"Ireland",
"Italy",
"Kosovo",
"Latvia",
"Liechtenstein",
"Lithuania",
"Luxembourg",
"Malta",
"Moldova",
"Monaco",
"Montenegro",
"Netherlands",
"Norway",
"Poland",
"Portugal",
"Romania",
"Russia", 
"San Marino",
"Serbia",
"Slovakia",
"Slovenia",
"Spain",
"Sweden",
"Switzerland",
"Turkey",
"Ukraine",
"United Kingdom",
"Vatican City"
]

try:
    oil_production_data_europe = pd.read_csv('data/total_oil_production_europe.csv')
except FileNotFoundError:
    oil_production_data_europe = create_oil_production_dataset_countries(oil_production_data, countries_in_europe)
    oil_production_data_europe.to_csv('data/total_oil_production_europe.csv', index=False)