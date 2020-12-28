import mysql.connector
from utils.HostController import HostController
from errors.DatabaseError import TableCreateError


class ColumnStructure:

    @property
    def auto_increment(self):
        return self._auto_increment

    @property
    def comments(self):
        return self._comments

    def __init__(self):
        self.__types = ['VARCHAR', 'TEXT', 'DATE', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'BIGINT', 'DECIMAL',
                        'FLOAT', 'DOUBLE', 'REAL', 'BIT', 'BOOLEAN', 'SERIAL', 'DATE', 'DATETIME', 'DATESTAMP',
                        'TIME', 'YEAR', 'CHAR', 'VARCHAR', 'TINYTEXT', 'MEDIUMTEXT', 'LONGTEXT', 'BINARY'
                                                                                                 'VARBINARY',
                        'TINYBLOB', 'BLOB', 'MEDIUMBLOB', 'LONGBLOB', 'ENUM', 'SET']
        self.__attributes_values = ['BINARY', 'UNSIGNED', 'UNSIGNED ZEROFILL', 'ON UPDATE CURRENT_TIMESTAMP']
        self.name = ''
        self.type = 'INT'
        self.length = 11
        self.default = ''
        self.collation = None
        self.attributes = ''
        self.is_null = False
        self._index = ''
        self._comments = None
        self.virtuality = None
        self._auto_increment = ''

    def set_index(self, index):
        self._index = index

    def get_index(self):
        return self._index

    def delete_index(self):
        del self._index

    index = property(get_index, set_index)

    @auto_increment.setter
    def auto_increment(self, value):
        if value:
            self.index = "PRIMARY"
            self._auto_increment = "AUTO_INCREMENT"
        else:
            self._auto_increment = ""

    @auto_increment.getter
    def auto_increment(self):
        return self._auto_increment

    @auto_increment.deleter
    def auto_increment(self):
        del self._auto_increment

    @comments.setter
    def comments(self, value):
        if value == '':
            self._comments = ''
        else:
            self._comments = "COMMENT '%s'" % value

    @comments.getter
    def comments(self):
        return self._comments

    def __str__(self):
        if self.name == '':
            raise TableCreateError("Choose a name for column")
        elif (self.type is None) or self.type.upper() not in self.__types:
            raise TableCreateError("Invalid %s type this column" % self.type)
        elif self.attributes != '' and self.attributes.upper() not in self.__attributes_values:
            raise TableCreateError("Invalid attribute value: %s" % self.__attributes_values)

        index = ''
        if self.index.upper() == 'PRIMARY':
            index = ', PRIMARY KEY(`%s`)' % self.name

        col_type = '%s(%s)' % (self.type, self.length)
        if self.type.upper() in ['DATE', 'DATETIME', 'DATESTAMP',
                                 'TIME', 'YEAR']:
            col_type = self.type

        query = "`%s` %s %s %s %s %s %s %s" % (
            self.name, col_type, self.attributes, "NULL" if self.is_null else "NOT NULL",
            self._auto_increment, self.default, self.comments, index)
        return query


class TableStructure:

    def __init__(self):
        self.name = ""
        self.engine = "INNODB"
        self.collation = ""
        self.comment = ""
        self.__columns = []

    def __str__(self):
        query = "CREATE TABLE %s (%s) ENGINE=%s" % (self.name, self._get_columns(), self.engine)
        if self.comment != '':
            query = query + " COMMENT='%s'" % self.comment

        return query

    def _get_columns(self):
        query = ""
        for column in self.__columns:
            if query == "":
                query = str(column)
            else:
                query = query + ", " + str(column)
        return query

    def append_column(self, column: ColumnStructure):
        self.__columns.append(column)


class DatabaseController:
    def __init__(self, host, username, password, database, create_database=False):
        if create_database:
            host_ctrl = HostController(host, username, password)
            host_ctrl.create_database_if_exists(database)
        self.host = host
        self.user = username
        self.password = password
        self.database = database
        self.db = mysql.connector.connect(host=host, user=username, password=password, database=database)

    def create_table(self, table_structure: TableStructure):
        cursor = self.db.cursor()
        cursor.execute(str(table_structure))

    def drop_table(self, table: str):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE `%s`" % table)

    def rename_table(self, from_name: str, to_name):
        cursor = self.db.cursor()
        cursor.execute("RENAME TABLE '%s' TO '%s'" % (from_name, to_name))

    def add_column_to_table(self, table, column: ColumnStructure):
        query = "ALTER TABLE %s ADD COLUMN %s" % (table, str(column))
        cursor = self.db.cursor()
        cursor.execute(query)

    def drop_column_from_table(self, table, column_name):
        query = "ALTER TABLE %s DROP COLUMN `%s`" % (table, column_name)
        cursor = self.db.cursor()
        cursor.execute(query)

    def drop_database(self):
        query = "DROP DATABASE IF EXISTS %s" % self.database
        cursor = self.db.cursor()
        cursor.execute(query)
