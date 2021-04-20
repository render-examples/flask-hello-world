import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
from selenium import webdriver
from time import sleep 
import glob
from dotenv import load_dotenv, find_dotenv
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import connect_to_db

# Web scraping from B3 website 
load_dotenv()

executable_path = os.environ.get("DRIVER_EXECUTABLE_PATH")

url = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br" 
driver = webdriver.Chrome(executable_path)
driver.get(url)
sleep(5)

driver.find_element_by_link_text("Download").click()
sleep(5)

driver.close()

downloads_dir_path = os.environ.get("DOWNLOADS_DIR_PATH")
path_to_file = glob.glob(f"{downloads_dir_path}*.csv")
latest_file = max(path_to_file, key=os.path.getctime)

df = pd.read_csv(
    latest_file,
    sep=";",
    encoding="latin-1",
    engine="python",
    skipfooter=2,
    thousands=".",
    decimal=",",
    header=1,
    index_col=False
    ) 

# POPULATING ASSET TABLE  
asset = df.loc[:, ["Código", "Ação", "Tipo"]].copy()
asset['YF_Código'] = asset['Código'] + '.SA'

# Writing the SQL query to populate asset table
insert_initial = """
    INSERT INTO asset (symbol, name, type, yf_symbol)
    VALUES
"""

values = ",".join([
    "('{}', '{}', '{}', '{}')"
        .format(row.Código, row.Ação, row.Tipo, row.YF_Código) 
    for symbol, row in asset.iterrows()
])

insert_end = """
    ON CONFLICT (symbol) DO UPDATE 
    SET
    symbol = EXCLUDED.symbol,
    name = EXCLUDED.name,
    type = EXCLUDED.type,
    yf_symbol = EXCLUDED.yf_symbol;
"""

query = insert_initial + values + insert_end

# Executing the query 
engine = connect_to_db()
engine.execute(query)


# POPULATING ASSET_PORTFOLIO TABLE 

# Importing asset and portfolio tables from PostgreSQL 
asset_from_sql = pd.read_sql('asset', engine, columns=['id','symbol'])
portfolio_from_sql = pd.read_sql('portfolio', engine)

# Creating 'asset_id' and 'portfolio_id' columns on asset_portfolio dataframe
asset_portfolio = asset_from_sql.copy()[["id"]]
asset_portfolio.rename(columns={"id": "asset_id"}, inplace=True)
asset_portfolio["portfolio_id"] = int(portfolio_from_sql.loc[portfolio_from_sql["name"] == "IBOV", 'id'])

# Creating the 'weight' column
participation = df.loc[:, ["Código", "Part. (%)"]].copy()
participation.rename(columns={"Código": "symbol",  "Part. (%)": "weight"}, inplace=True)
participation["weight"] = participation["weight"] / 100
# Merging participation and asset_from_sql ON symbol   
# and isolating only the columns 'asset_id' and 'weight'
participation = asset_from_sql.merge(participation, how='inner', on='symbol')
participation.drop(columns=["symbol"], inplace=True)
participation.rename(columns={"id": "asset_id"}, inplace=True)

# Merging participation and asset_portfolio dataframes ON 'asset_id' column
# in order to get the three columns together and complete asset_portfolio table 
asset_portfolio = asset_portfolio.merge(participation, how='inner', on='asset_id')

# Writing the SQL query to populate asset_portfolio table
insert_init = """
    INSERT INTO asset_portfolio (asset_id, portfolio_id, weight)
    VALUES
"""

values = ",".join(["('{}', '{}', '{}')"
        .format(int(row["asset_id"]), int(row["portfolio_id"]), round(row["weight"], 7)) 
    for asset_id, row in asset_portfolio.iterrows()
])

insert_end = """
    ON CONFLICT (asset_id, portfolio_id) DO UPDATE 
    SET
    asset_id = EXCLUDED.asset_id,
    portfolio_id = EXCLUDED.portfolio_id,
    weight = EXCLUDED.weight;
"""

query = insert_init + values + insert_end

engine.execute(query)

print("Script Successfully Executed!")