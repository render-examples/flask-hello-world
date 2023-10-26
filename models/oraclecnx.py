import cx_Oracle

class Oraclecnx:
    def dbcon(connection):
# Informations de connexion
        host = "localhost"
        port = 1521
        service_name = "ORCLCDB"

# Créer une connexion
        connection = cx_Oracle.connect(user="c##iagora", password="iagora", dsn=f"{host}:{port}/{service_name}")

# Afficher le nom de la base de données
        print(connection.database)
        return connection
