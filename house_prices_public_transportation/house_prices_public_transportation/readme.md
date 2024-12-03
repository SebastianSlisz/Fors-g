## Exam project in Introduction to Social Data Science
This folder is for our exam project on the course Introduction to social data science. The project is about the relationship between public transportation accessibility and the price of housing in Copenhagen.

## Overview of the files in the folder
**scraping.ipynb**: *This file was used to scrape data on busroutes and busstops from DOT, data on metrostops from M.dk, data on listed properties from Boligsiden. It stores the data in the folder "data/raw".*

**process.ipynb**: *This file is use to handle the raw data and generate the processed data. It utilizes the functions in the module "process.py". Generally it reads the raw data, processes it and stores the processed data in the folder "data".*

**analys.ipynb**: *This file is used to analyze the processed data. It generally reads the processed data, analyzes it and generates tables, figures and other output used in the attached PDF. Tables are stored in the folder "tables" and figures are stored in the folder "figs".*

## Packages used
The following packages are used in this project:
- pandas
- geopandas
- numpy
- matplotlib
- seaborn
- plotly
- statsmodels
- requests 
- bs4
- json
- time
- os
- re
- sklearn
- geopy
- googlemaps

