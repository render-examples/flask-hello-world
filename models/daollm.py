from langchain import OpenAI, Cohere, sql_database
from langchain_experimental.sql import SQLDatabaseChain
import cx_Oracle
import os
from langchain.chains import load_chain
import os

COHERE_API_KEY="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"
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

lib_dir = os.path.join(os.environ.get("HOME"), "Development", "instantclient_19_8")
cx_Oracle.init_oracle_client(lib_dir=lib_dir)

hostname='localhost'
port='1521'
service_name='ORCLCDB'
username='c##iagora'
password='iagora'

cx_Oracle.init_oracle_client(lib_dir=lib_dir)
oracle_connection_string_fmt = (
  'oracle+cx_oracle://{username}:{password}@' +
  cx_Oracle.makedsn('{hostname}', '{port}', service_name='{service_name}')
)
url = oracle_connection_string_fmt.format(
  username=username, password=password, 
  hostname=hostname, port=port, 
  service_name=service_name,
)
from sqlalchemy import create_engine
engine=create_engine(url, echo=True)
db = SQLDatabase(engine)
llm = Cohere(temperature=1, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
db_chain.run("Is Casey Brown in the database?")