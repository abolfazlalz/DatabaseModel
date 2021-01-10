from utils.ConfigController import ConfigController
from utils.TableController import TableController


class Model:
    columns = ['id']
    private_columns = []

    @staticmethod
    def __get_columns():
        return []

    @staticmethod
    def __get_private_columns():
        return []

    def __init__(self):
        config_ctrl = ConfigController()
        host = config_ctrl.configs['config']['host']
        username = config_ctrl.configs['config']['username']
        password = config_ctrl.configs['config']['password']
        database = config_ctrl.configs['config']['database']
        self.table = self.__class__.__name__
        self._table_ctrl = TableController(host=host, user=username, password=password, database=database,
                                           table=self.table)
        self._primary_key = 'id'
        self._time_stamps = True

    def __get_class_attr(self):
        attributes = dict(self.__dict__)
        attributes.pop('model')
        return attributes

    @staticmethod
    def find(m_id):
        models = [cls() for cls in Model.__subclasses__()]
        if len(models) == 0:
            model = Model()
        else:
            model = models[0]

        result = model._table_ctrl.select.where('id', m_id).get()[0].items()

        if len(result) == 0:
            return None
        else:
            for key, value in result:
                if key not in Model.__get_private_columns():
                    setattr(model, key, value)

            return model

    def save(self):
        pass
