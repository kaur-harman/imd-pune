This repository contains code to scrape tables for all stations in all the given years from imd-pune website. It also consolidates the scraped data into a single dataset.

```
      
├── README.md               <- The top-level README for developers using this project.
├── data
│   └── raw                 <- All the data scraped by "table_scraper.py" and "consolidated_data.py" is stored here.
│
└── src                     <- Source code for use in this project.
    ├── __init__.py         <- Makes src a Python module
    │
    └── data                <- Scripts to download or generate data
        ├── table_scraper.py       <- Script to scrape tables for all stations for all the given years on imd-pune. 
        └── consolidated_data.py   <- Script to consolidate all the data scraped by table_scraper.py into a single file which is stored in the raw folder by the name "consolidated_data.csv"

```