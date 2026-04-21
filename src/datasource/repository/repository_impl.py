# from datasource.repository.repository_interface import Repository
# from domain.model.game import CurrentGame
# from datasource.model.storage import Storage
# from datasource.mapper.mapper import Mapper
# from datasource.database.database import User
#
#
#
# class GameRepository(Repository):
#     """
#     Реализация сервиса с использованием репозитория.
#     """
#
#     def __init__(self, storage: Storage, session_db):
#         self._storage = storage
#         self.session_db = session_db
#
#     def save(self, game: CurrentGame) -> None:
#         """
#         Преобразует Game в DTO.
#         Сохраняет в хранилище.
#         """
#         game_dto = Mapper.from_domain_to_storage(game)
#
#         ## здесь должна происходить запись в БД
#         user_name = game_dto.user_info.name
#         user_pass = game_dto.user_info.password_hash
#
#         new_user = User(user_name=user_name, hashed_password=user_pass)
#         self.session_db.add(new_user)
#         self.session_db.commit()
#         self.session_db.close()
#
#         self._storage.add(game_dto)
#
#     def get(self, game_id) -> CurrentGame:
#         """
#         Извлекает DTO из хранилища.
#         Преобразует DTO в domain с помощью маппера.
#         """
#         game_dto = self._storage.get(game_id)
#         if game_dto is None:
#             print(f"REPOSITORY: Игра {game_id} не найдена в хранилище")
#             return None
#
#         return Mapper.from_storage_to_domain(game_dto)
