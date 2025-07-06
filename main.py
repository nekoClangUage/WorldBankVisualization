# -----------------------
# LIBRARIES

# MATH LIBRARIES (CUSTOM LIBRARIES)
import matplotlib.pyplot as plt

# STANDARD LIBRARY
import os
from lxml import etree as ET
# -----------------------


# GLOBAL VARIABLES
# -----------------------
TARGET_YEAR      = '2020'
NUM_OF_COUNTRIES = 10
XML_DATA_PATH    = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gdp_lcu_worldbank.xml')

DESC = True # Descending or Ascending of list of countries
COUNTRY_NAMES_OR_TAG = False # COUNTRY_NAMES = True; TAGS = False
# -----------------------

def parseXMLGDP(xml_path : str):
    if (not os.path.exists(xml_path)):
        raise ValueError('BAD_XML_DATA_PATH')

    with open(xml_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    xml_data = ET.fromstring(xml_content) # type: ignore
    return xml_data

def findRecordsByYear(xml_data, Year : str = TARGET_YEAR): # type: ignore
    return xml_data.xpath(f'./data/record[field[@name="Year" and text()="{Year}"]]')

def createDiagram(xml_data, target_year : str, number_countries : int):
    records_by_year = findRecordsByYear(xml_data, target_year)

    countries_and_gdp = []

    for record in records_by_year:
        fields = record.xpath('./field')
        
        country = record.xpath('./field[@name="Country or Area"]/' + ('text()' if COUNTRY_NAMES_OR_TAG else '@key'))[0]
        item = record.xpath('./field[@name="Item"]/text()')[0]
        year = record.xpath('./field[@name="Year"]/text()')[0]
        value = record.xpath('./field[@name="Value"]/text()')    # Can be null
        
        if(len(value) == 1):
            countries_and_gdp.append((country, float(value[0])))
    
    countries_and_gdp.sort(key = lambda item: item[1])
    
    name_of_countries = [item[0] for item in countries_and_gdp]
    value_of_gdp_countries = [item[1] for item in countries_and_gdp]

    figure, axes = plt.subplots(figsize=(20, 20))

    color_val, edgecolor_val, width_val = 'purple', 'black', 0.2

    if(DESC):
        bar_diagram = axes.bar(
            x=name_of_countries[-number_countries:],           
            height=value_of_gdp_countries[-number_countries:], 
        
            color=color_val,
            edgecolor=edgecolor_val,
            width=width_val             
        )
    else:
        bar_diagram = axes.bar(
            x=name_of_countries[:number_countries],           
            height=value_of_gdp_countries[:number_countries], 
        
            color=color_val,
            edgecolor=edgecolor_val,
            width=width_val             
        )

    axes.set_title (f"GDP (LCU) per country in The World ({target_year})")
    axes.set_xlabel("Country name (tag)")
    axes.set_ylabel("GDP (LCU) value")
    axes.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

if __name__ == '__main__':
    parsed_data = parseXMLGDP(XML_DATA_PATH)
    createDiagram(parsed_data, TARGET_YEAR, NUM_OF_COUNTRIES)
