# from domain.model.game import CurrentGame
# from datasource.repository.repository_backed_service import RepositoryBackedService
# from datasource.repository.repository_impl import GameRepository
# from domain.helpers.prints import *
from datasource.model.storage import Storage
from web.app import create_app


# def main():
#     """"Функция для запуска игры в терминале"""
#     print_previe()
#     storage = Storage()
#     repository = GameRepository(storage)
#     repository_game_service = RepositoryBackedService(repository)
#     game = CurrentGame()
#     print_field(game.field)
#
#     while True:
#
#         step_human(game)
#         print_field(game.field)
#         repository_game_service.get_next_step(game)
#         print_field(game.field)
#         if repository_game_service.is_game_over(game):
#             break

def main():
    """"Функция main для web слоя"""
    storage = Storage()
    app = create_app(storage)
    print("Сервер запущен. http://localhost:5000")
    # print("Открой в браузере: http://localhost:5000/create_game")
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
