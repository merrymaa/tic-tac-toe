from datasource.model.game_dto import GameDTO
from threading import Lock


class Storage():
    """
    Класс Хранилище (singleton).
    Хранит информацию об игре в виде словаря: ключ - UUID игры, значение - GameDTO
    """
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.game_storage = {}
            self._storage_lock = Lock()
            self._initialized = True

    def add(self, game_dto) -> None:

        """
        Сохранение DTO в словарь хранилища
        """
        with self._lock:
            self.game_storage[str(game_dto.uuid)] = game_dto
            print(f"STORAGE: Игра сохранена. UUID: {game_dto.uuid}")
            for key, value in self.game_storage.items():
                print(f"uuid: {str(key)} - {value.field.field}")
                # print(key, ': ', value)

    def get(self, game_id: str) -> GameDTO:
        """
        Извлечение игры из словаря хранилища и возвращение в формате GameDTO
        """
        with self._lock:
            try:
                if self.game_storage[game_id]:
                    print(f"STORAGE: Игра найдена. UUID: {game_id}")
                    return self.game_storage[game_id]
                else:
                    print(f"STORAGE: Игра с UUID {game_id} не найдена.")
                    return
            except Exception as e:
                print(f"Ошибка в Хранилище - {e}")
