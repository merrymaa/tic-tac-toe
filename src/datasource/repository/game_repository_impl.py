from datasource.database.database import Games, SessionLocal, User
from datasource.repository.game_repository_interface import GameRepository
from domain.model.game import CurrentGame
from datasource.mapper.mapper import Mapper


class GameRepositoryImpl(GameRepository):
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def save_game(self, game: CurrentGame) -> None:
        with self.session_factory() as session:
            db_game = session.query(Games).filter(Games.uuid == game.uuid).first()
            if db_game:
                db_game.field = game.field.field
                db_game.status = game.status
                db_game.type = game.type
                db_game.step_player = game.step_player
                db_game.player_1_uuid = game.player_1_uuid
                db_game.player_2_uuid = game.player_2_uuid
                db_game.player_1_sign = game.player_1_sign
                db_game.player_2_sign = game.player_2_sign
                db_game.draw = game.draw
                db_game.winner = game.winner
            else:
                new_game = Games(
                    uuid=game.uuid,
                    field=game.field.field,
                    status=game.status,
                    type=game.type,
                    step_player=game.step_player,
                    player_1_uuid=game.player_1_uuid,
                    player_2_uuid=game.player_2_uuid,
                    player_1_sign=game.player_1_sign,
                    player_2_sign=game.player_2_sign,
                    draw=game.draw,
                    winner=game.winner
                )
                session.add(new_game)
            session.commit()

    def add_game(self, game: CurrentGame) -> None:
        session_db = self.session_factory()
        # CurrentGame -> Games
        game_dt_src = Mapper.domain_to_datasource(game)
        session_db.add(game_dt_src)
        session_db.commit()
        session_db.close()

    def get_active_games(self) -> list[Games]:
        with self.session_factory() as session:
            active_games = session.query(Games).filter(
                Games.winner.is_(None),
                Games.draw.is_(None)
            ).all()
            return active_games

    def get_current_game(self, game_uuid: str) -> Games:
        with self.session_factory() as session:
            current_game = session.query(Games).filter(Games.uuid == game_uuid).first()
            return current_game

    def get_user(self, user_uuid) -> User:
        with self.session_factory() as session:
            current_user = session.query(User).filter(User.uuid == user_uuid).first()
            return current_user

    def get_available_games(self, player_uuid: str) -> list[Games]:
        """"Возвращает игры доступные для присоединения игроку player_uuid"""
        with self.session_factory() as session:
            available_games = session.query(Games).filter(Games.status == "waiting", Games.type == "HUMAN",
                                                          Games.player_2_uuid.is_(None),
                                                          Games.player_1_uuid != player_uuid).all()
            return available_games

    def get_game(self, game_uuid: str) -> CurrentGame:
        with self.session_factory() as session:
            game = session.query(Games).filter(Games.uuid == game_uuid).first()
            current_game = CurrentGame()

            current_game.uuid = game.uuid
            current_game.field.field = game.field
            current_game.status = game.status
            current_game.type = game.type
            current_game.step_player = game.step_player
            current_game.player_1_uuid = game.player_1_uuid
            current_game.player_2_uuid = game.player_2_uuid
            current_game.player_1_sign = game.player_1_sign
            current_game.player_2_sign = game.player_2_sign
            current_game.draw = game.draw
            current_game.winner = game.winner
        return current_game
