import pandas as pd
from data_reading import create_oil_production_dataset_countries, preprocess_data
from data_reading import create_oil_production_dataset


try:
    processed_data = pd.read_csv('data/processed_data.csv')
except FileNotFoundError:
    processed_data = preprocess_data()
    processed_data.to_csv('data/processed_data.csv', index=False)

try:
    oil_production_data = pd.read_csv('data/total_oil_production.csv')
except FileNotFoundError:
    oil_production_data = create_oil_production_dataset(processed_data)
    oil_production_data.to_csv('data/total_oil_production.csv', index=False)





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
"Russia", #Include russia?
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