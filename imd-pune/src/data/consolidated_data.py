import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
import re
import numpy as np
import glob
import csv
import pandas as pd

class Consolidate:
    """
        Class used to consolidate the data scraped in raw folder into a single csv file saved in raw directory
    
    """
    
    def __init__(self):
        """
            Initialize class and defines directory paths
        """
        
        self.dir_path = Path.cwd()
        self.raw_path = Path.joinpath(self.dir_path, "data", "raw")
        self.json_path = Path.joinpath(self.raw_path, "json")
        if not self.json_path.exists():
            Path.mkdir(self.json_path, parents=True, exist_ok=True)
        self.station_file_path = Path.joinpath(self.json_path, "station.json")
        self.consolidated_data_path = Path.joinpath(self.raw_path, "consolidated_data.csv")
        
    
    def concat_tables(self):
        """
        Concatenates multiple CSV tables into a single table.

        This function reads all the CSV files in the specified directory and concatenates them into a single DataFrame.
        The resulting DataFrame is then saved as a CSV file in the raw directory.
        
        """
        data=[]
        first_table =True
        dataframe=[]
        for file_path in self.raw_path.glob("**/*.csv"):
            df = pd.read_csv(file_path)
            if first_table:
                dataframe.append(df)
                first_table = False
            else:
                dataframe.append(df[1:])
                
        compiled_data = pd.concat(dataframe)
        compiled_data.to_csv(self.consolidated_data_path, index=False,encoding='utf-8-sig')
       
if __name__=="__main__":
    conc = Consolidate()
    conc.concat_tables()