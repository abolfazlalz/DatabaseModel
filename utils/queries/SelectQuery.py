from mysql.connector import MySQLConnection


class SelectQuery:
    _where_condition: str

    def __init__(self, table: str, db: MySQLConnection):
        self._columns = '*'
        self._where_condition = ""
        self._db = db
        self._table = table

    def where(self, key: str, value, operator="="):
        return self.__where(key, value, operator, "and")

    def or_where(self, key: str, value, operator="="):
        return self.__where(key, value, operator, "or")

    def __where(self, key: str, value, operator, condition):
        key = self.__fix_condition(key, value)['key']
        value = self.__fix_condition(key, value)['value']
        if self._where_condition == "":
            self._where_condition = "WHERE "
        else:
            self._where_condition = self._where_condition + " %s " % condition
        self._where_condition = self._where_condition + "%s %s %s" % (key, operator, value)
        return self

    def select_columns(self, columns: list):
        columns = [self.__fix_condition(column, '')['key'] for column in columns]
        if len(columns) == 0:
            self._columns = '*'
        else:
            self._columns = ', '.join(columns)
        return self

    def clear_where(self):
        self._where_condition = ""
        return self

    def get(self):
        cursor = self._db.cursor()
        cursor.execute(self.__get_query())
        result = []
        for item in cursor.fetchall():
            result.append(item)
        return result

    def __get_query(self):
        result = "SELECT %s FROM `%s` %s" % (self._columns, self._table, self._where_condition)
        return result

    def __str__(self):
        return self.__get_query()

    @staticmethod
    def __fix_condition(key: str, value):
        if '`' in key:
            if not key.endswith('`') or not key.startswith('`'):
                key = key.replace('`', '\\`')
            key = "`%s`" % key
        else:
            key = "`%s`" % key

        value = str(value)
        if not value.isnumeric():
            value = "'%s'" % value

        return {'key': key, 'value': value}
