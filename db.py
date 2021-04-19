import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv, find_dotenv

def connect_to_db():
    load_dotenv()

    user_name = os.environ.get("DB_USER_NAME")
    password = os.environ.get("DB_PASSWORD")
    endpoint = os.environ.get("DB_ENDPOINT")
    port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")

    address = "postgresql://{}:{}@{}:{}/{}".format(
        user_name,
        password,
        endpoint,
        port,
        db_name)

    engine = create_engine(address)
    
    return engine
