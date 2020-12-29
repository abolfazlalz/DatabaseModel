import mysql.connector
from utils.queries.SelectQuery import SelectQuery


class TableController:

    def __init__(self, host: str, user: str, password: str, database: str, table: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.table = table
        self.db = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.select = SelectQuery(table, self.db)

    def insert(self, data_list: dict):
        data_list = self.__fix_datalist_values__(data_list)
        columns_keys = ', '.join(data_list.keys())
        columns_values = ', '.join(data_list.values())

        query = "INSERT INTO %s (%s) VALUES (%s)" % (self.table, columns_keys, columns_values)
        cursor = self.execute_query(query)
        self.db.commit()
        return cursor.lastrowid

    def update(self, data_list: dict, condition: dict):
        data_list = self.__fix_datalist_values__(data_list)
        condition = self.__fix_datalist_values__(condition)
        data_list_result = ', '.join('='.join((key, val)) for (key, val) in data_list.items())
        condition_result = ', '.join('='.join((key, val)) for (key, val) in condition.items())

        query = "UPDATE %s SET %s WHERE %s" % (self.table, data_list_result, condition_result)
        self.execute_query(query)
        self.db.commit()

    def delete(self, condition: dict):
        condition = self.__fix_datalist_values__(condition)
        condition_result = ', '.join('='.join((key, val)) for (key, val) in condition.items())

    def execute_query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor

    @staticmethod
    def __give_str_value__(value: str) -> str:
        if not isinstance(value, str):
            return str(value)
        elif value.isnumeric():
            return value
        else:
            return "'%s'" % value.replace('\'', "\\'")

    @staticmethod
    def __fix_datalist_values__(data_list: dict):
        return {"`%s`" % key: TableController.__give_str_value__(val) for (key, val) in data_list.items()}

    def __get_where_condition__(self, where_data_list):
        condition = self.__fix_datalist_values__(where_data_list)
        condition_result = ', '.join('='.join((key, val)) for (key, val) in condition.items())
        return condition_result
