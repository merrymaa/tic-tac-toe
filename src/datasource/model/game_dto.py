from datasource.model.field_dto import FieldDTO


class GameDTO():
    """
    Data Transfer Object - Объект передачи данных между domain и хранилищем
    """

    def __init__(self):
        self.field = FieldDTO()
        self.uuid = None
