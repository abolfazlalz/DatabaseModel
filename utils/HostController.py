import mysql.connector
from errors.DatabaseError import DatabaseNotExistsError


class HostController:
    def __init__(self, host, username, password):
        self.db = mysql.connector.connect(host=host, user=username, password=password)

    def create_database(self, database: str):
        query = "CREATE DATABASE %s" % database
        cursor = self.db.cursor()
        cursor.execute(query)

    def create_database_if_exists(self, database: str):
        query = "CREATE DATABASE IF NOT EXISTS %s" % database
        cursor = self.db.cursor()
        cursor.execute(query)

    def drop_database(self, database: str):
        try:
            cursor = self.db.cursor()
            cursor.execute("DROP DATABASE %s" % database)
        except mysql.connector.errors.DatabaseError as error:
            if error.msg == 'Can\'t drop database \'abolfazl\'; database doesn\'t exist':
                raise DatabaseNotExistsError()

    def drop_database_if_exists(self, database: str):
        cursor = self.db.cursor()
        cursor.execute("DROP DATABASE IF EXISTS %s" % database)

    def database_exists(self, database: str):
        cursor = self.db.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s'" % database)
        result = []
        for database in cursor:
            result.append(database)
        return result

    def show_databases(self) -> list:
        cursor = self.db.cursor()
        cursor.execute("SHOW DATABASES")
        result = []

        for database in cursor:
            result.append(database[0])
        return result
