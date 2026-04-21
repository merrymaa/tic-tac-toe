# from sqlalchemy.orm import session
# from sqlalchemy import select
#
# from datasource.database.database import Games, SessionLocal
# from datasource.database.game_db_interface import GameDbInterface
#
#
# class GameDbImpl(GameDbInterface):
#     def __init__(self, session_factory=SessionLocal):
#         self.session_factory = session_factory
#
#     def save_game(self, game: Games):
#         session_db = self.session_factory()
#         session_db.add(game)
#         session_db.commit()
#         session_db.close()
#
#     def get_active_games(self):
#         with self.session_factory() as session:
#             active_games = session.query(Games).filter(
#                 Games.winner.is_(None),
#                 Games.draw.is_(None)
#             ).all()
#             return active_games
