from flask import Flask
from datetime import datetime
import psycopg2

app = Flask(__name__)

class mydb(object):
    dsn = None
    connection = None
    server = None
    usr = None
    pwd = None
    host = None
    port = 26257
    dbname = None
    explain_flag = 0

    def __init__(self, *args):
        pass

    def connect(self):
        # Sample connection parameters
        conn_params={ 
            "dsn" : "postgres://uc_dba:1kHsS51jDlND9RHSLQuEMDDCN0azZ9HQ@dpg-cfvqn202qv24oq7iibk0-a/unicomm",
            # "user" : "root",
            # "password" : "rtc;8993"
            # "host" : self.host,
            # "port" : self.port,
            # "database" : self.dbname
        }
        # Establish a connection
        self.connection = psycopg2.connect(**conn_params)
        self.server_version = self.connection.info.server_version
        self.dsn = self.connection.dsn
        print("Connected to Cockroach v%s via psycopg2 driver,"%self.server_version)
        print("DSN: %s"%self.dsn)

@app.route('/')
def hello_world():
    db = mydb()
    db.connect()
    return f'Hello, World!  Current Time: {str(datetime.now())} UTC'