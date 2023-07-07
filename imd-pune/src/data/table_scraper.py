import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import re

class Scraper:
    """
        Class to scrape data from imd-pune website.
    """
    
    def __init__(self):
        """
            Initialize class Scraper and defines paths for raw_directory and directory where scraped tables are to be stored
        """
        
        self.dir_path = Path.cwd()
        self.raw_path = Path.joinpath(self.dir_path, "data", "raw")
        if not self.raw_path.exists():
            Path.mkdir(self.raw_path, parents=True, exist_ok=True)
        self.json_path = Path.joinpath(self.raw_path, "json")
        if not self.json_path.exists():
            Path.mkdir(self.json_path, parents=True, exist_ok=True)
        self.station_file_path = Path.joinpath(self.json_path, "station.json")
        self.empty_table = Path.joinpath(self.json_path, "empty_table.json")
        

    def scrape_stations(self):
        """
            Scrapes station data (station_name and station_code) and saves it to a JSON file
        """
        stations = []
        if response.status_code == 200:
            self.station_select = soup.find('select', {'name': 'stn_index'})
            self.options = self.station_select.find_all('option')[2:]

            for option in self.options:
                station_name = option.text.split(' [')[0]
                station_code = option['value']
                if station_name != '' and station_code != '':
                    stations.append({
                        'station_name': station_name,
                        'station_code': station_code
                    })
        else:
            print('Request failed with status code:', response.status_code)

        with open (str(self.station_file_path), "w") as f:
            json.dump(stations, f)
    
    def select_all_parameters(self):
        """
        Selects timescale, year, parameter and stations and scrapes corresponding table for each station and saves them as CSV files.
        """
        with open(str(self.station_file_path), "r") as f:
            self.station = json.load(f)
        # empty=[]
        # unique = set()
        year_from_select = soup.find('select', {'name': 'year_from'})
        years_from = [option['value'] for option in year_from_select.find_all('option') if option['value'] != '']
        for year in years_from:
            year_folder = Path.joinpath(self.raw_path, year)
            if not year_folder.exists():
                Path.mkdir(year_folder,parents=True)
            parameter_select = soup.find('select', {'name': 'parameter'})
            parameter_options = parameter_select.find_all('option')[2:4]
            for param in parameter_options:
                parameter_text=param.text
                parameter = param['value']
           
                parameter_name_corrected = parameter_text.replace(" ", "_").lower()
                parameter_folder_path = Path.joinpath(year_folder, parameter_name_corrected)
                if not parameter_folder_path.exists():
                    Path.mkdir(parameter_folder_path,parents=True)
                for option in self.options:
                    for row in self.station:
                        station_name_corrected = re.sub(r"[^A-Za-z0-9_]", "", row["station_name"].lower().strip().replace(" ", "_"))
                        table_path = Path.joinpath(parameter_folder_path, f"{station_name_corrected}.csv")
                        if not table_path.exists():
                            print(f"Proceeding to scrape table for {station_name_corrected} for {year}")
                            if option['value']== row["station_code"]:
                                data={
                                    'timescale': 'monthly',
                                    'parameter': parameter,
                                    'stn_index': row['station_code'],
                                    'year_from': year,
                                    'year_to': year
                                }
                                response = requests.post(url, data=data)
                                if response.status_code == 200:
                                    
                                    table = pd.read_html(response.text, header=0)[0]
                                    table.columns = [x.lower().replace(' ', '_') for x in table.columns]
                                    table.insert(0,"year", year)
                                    table.insert(1, "station_name", station_name_corrected)
                                    table.insert(2, "station_code", row['station_code'])
                                    table.insert(3, 'parameter', parameter_text)
                                    print(table)
                                    table.to_csv(Path.joinpath(parameter_folder_path, f"{station_name_corrected}.csv"),index=False,encoding='utf-8-sig')
                                    print(f" Scraped station {station_name_corrected} table for {year}")
                    
                        else:
                            print(f"Table for {station_name_corrected} for {year} already exists")        
    
if __name__ == '__main__':
    url = "https://cdsp.imdpune.gov.in/home_riturang_sn.php#snormals"
    scraper = Scraper()
    while True:
        try:
            scraper = Scraper()
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            scraper.scrape_stations()
            scraper.select_all_parameters()
            break
        except requests.exceptions.ConnectionError:
            print("Connection error occurred. Retrying...")
            continue
        except Exception as e:
            print("Error occurred:" + str(e))

    