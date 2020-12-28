class DatabaseError(Exception):
    def __init__(self, *args: object):
        self.msg = None

    def __str__(self):
        return self.msg


class DatabaseNotExistsError(DatabaseError):
    def __init__(self):
        self.msg = "can't found database"


class DatabaseBadNameError(DatabaseError):
    def __init__(self):
        self.msg = "Bad database name"


class TableCreateError(DatabaseError):
    def __init__(self, msg):
        self.msg = msg
