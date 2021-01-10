from pathlib import Path

from Model import Model
from utils.DatabaseController import ColumnStructure
from utils.DatabaseController import DatabaseController
from utils.DatabaseController import TableStructure
from utils.TableController import TableController


class User(Model):
    id: int
    name: str

    def __init__(self):
        self.id = 0
        self.name = ""
        self.birthday = ""
        super().__init__()

    def __str__(self):
        return "Hello my name is %s and my birthday is %s" % (self.name, self.birthday)


def create_user_table():
    host = 'localhost'
    user = 'root'
    password = ''
    database = "test_db"
    table_name = 'users'
    database_ctrl = DatabaseController(host, user, password, database, create_database=True)

    column_id = ColumnStructure()
    column_id.type = 'int'
    column_id.name = 'id'
    column_id.auto_increment = True
    column_id.comments = "id of user"

    column_name = ColumnStructure()
    column_name.type = 'varchar'
    column_name.length = 50
    column_name.name = "name"
    column_name.comments = "the name of user"

    column_birth = ColumnStructure()
    column_birth.type = 'date'
    column_birth.name = "birthday"
    column_birth.comments = "date of birthday of user"

    table = TableStructure()
    table.name = table_name
    table.append_column(column_id)
    table.append_column(column_name)
    table.append_column(column_birth)
    table.comment = "users table"

    database_ctrl.create_table(table)


def new_user(name: str, birthday: str):
    data_list = {'name': name, 'birthday': birthday}
    return get_table_connection().insert(data_list)


def update_user(name: str, birthday: str, user_id: int):
    data_list = {'name': name, 'birthday': birthday}
    return get_table_connection().update(data_list, {'id': user_id})


def get_table_connection():
    host = 'localhost'
    user = 'root'
    password = ''
    database = "test_db"
    table_name = 'users'
    table_ctrl = TableController(host, user, password, database, table_name)
    return table_ctrl


def get_db_connection():
    host = 'localhost'
    user = 'root'
    password = ''
    database = "test_db"
    db = DatabaseController(host, user, password, database, create_database=True)
    return db


def drop_table():
    host = 'localhost'
    user = 'root'
    password = ''
    database = "test_db"
    table_name = 'users'
    database_ctrl = DatabaseController(host, user, password, database, create_database=True)
    database_ctrl.drop_table(table_name)
    pass


def drop_column():
    db = get_db_connection()
    db.drop_column_from_table('users', 'birthday')


def select_query():
    table = get_table_connection()
    print(table.select.where("id", 0, '>').select_columns(['name', 'id']).get())


if __name__ == '__main__':
    # drop_table()
    # create_user_table()
    # new_user("Abolfazl Alizadeh", "2002-12-3")
    # new_user("Masood Lotfian", "2002-12-1")
    # new_user("Matin Dehghanian", "2003-9-25")
    # select_query()
    user = User.find(12)
    pass
