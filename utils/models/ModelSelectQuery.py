from mysql.connector import MySQLConnection

from utils.queries.SelectQuery import SelectQuery


class ModelSelectQuery(SelectQuery):

    def __init__(self, m_type, table: str, db: MySQLConnection):
        super().__init__(table, db)
        self._type = m_type

    def get(self):
        selects = super(ModelSelectQuery, self).get()
        models = []
        for select in selects:
            model = self._type.__class__

            for key, value in select.items():
                setattr(model, key, value)
            models.append(model)
        return models
