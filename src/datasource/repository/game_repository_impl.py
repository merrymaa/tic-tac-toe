import datetime
from sqlalchemy import select, func, cast, Float
from datasource.database.database import Games, SessionLocal, User, Leaderboard
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
                db_game.date_created = game.date_created
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
                    date_created=datetime.datetime.now(),
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

    # def get_finished_games(self) -> list[Games]:
    #     with self.session_factory() as session:
    #         finished_games = session.query(Games).filter(
    #             Games.status == "finish"
    #         ).all()
    #         return finished_games

    def get_finished_games(self, user_uuid: str) -> list[Games]:
        with self.session_factory() as session:
            finished_games = session.query(Games).filter(
                Games.status == "finish",
                (Games.player_1_uuid == user_uuid) | (Games.player_2_uuid == user_uuid)
            ).all()
            return finished_games

    def get_current_game(self, game_uuid: str) -> Games:
        with self.session_factory() as session:
            current_game = session.query(Games).filter(Games.uuid == game_uuid).first()
            return current_game

    def get_user(self, user_uuid: str) -> User:
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
            current_game.date_created = game.date_created
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

    def get_statistic(self, n: int) -> dict:
        """"
        Выполняется SQL-запрос:
        with
            winners as (
                select player_1_uuid as user_uuid, count(*) as count_wins
                from games
                where player_1_uuid = winner and status = 'finish'
                group by player_1_uuid
                union
                select player_2_uuid, count(*) as count_wins
                from games
                where player_2_uuid = winner and status = 'finish'
                group by player_2_uuid
                ),
            fails as (
                select winner as fails, count(*)
                from games
                where status = 'finish' and player_1_uuid != winner
                group by winner
                having winner != 'false'
                union
                select winner, count(*)
                from games
                where status = 'finish' and player_2_uuid != winner
                group by winner
                having winner != 'false'
            ),
            draws as (
                select player_1_uuid as user_uuid, count(draw)
                from games
                where draw = 'true'
                group by player_1_uuid
                union
                select player_2_uuid, count(draw)
                from games
                where draw = 'true'
                group by player_2_uuid
                )
        select
            w.user_uuid,
            (w.count_wins::float / (d.count::float + f.count::float)) as ratio
        from winners as w
        join draws as d on w.user_uuid = d.user_uuid
        join fails as f on w.user_uuid = f.fails
        order by ratio desc
"""

        wins_p1 = (
            select(Games.player_1_uuid.label("user_uuid"), func.count().label("count_wins"))
            .where(Games.player_1_uuid == Games.winner, Games.status == "finish")
            .group_by(Games.player_1_uuid)
        )
        wins_p2 = (
            select(Games.player_2_uuid.label("user_uuid"), func.count().label("count_wins"))
            .where(Games.player_2_uuid == Games.winner, Games.status == "finish")
            .group_by(Games.player_2_uuid)
        )
        winners_cte = wins_p1.union(wins_p2).cte("winners")

        fails_p1 = (
            select(Games.winner.label("fails"), func.count().label("count"))
            .where(Games.status == "finish", Games.player_1_uuid != Games.winner)
            .group_by(Games.winner)
            .having(Games.winner != "false")
        )
        fails_p2 = (
            select(Games.winner.label("fails"), func.count().label("count"))
            .where(Games.status == "finish", Games.player_2_uuid != Games.winner)
            .group_by(Games.winner)
            .having(Games.winner != "false")
        )
        fails_cte = fails_p1.union(fails_p2).cte("fails")

        draws_p1 = (
            select(Games.player_1_uuid.label("user_uuid"), func.count(Games.draw).label("count"))
            .where(Games.draw == "true")
            .group_by(Games.player_1_uuid)
        )
        draws_p2 = (
            select(Games.player_2_uuid.label("user_uuid"), func.count(Games.draw).label("count"))
            .where(Games.draw == "true")
            .group_by(Games.player_2_uuid)
        )
        draws_cte = draws_p1.union(draws_p2).cte("draws")

        ratio = (
                cast(winners_cte.c.count_wins, Float) /
                (cast(draws_cte.c.count, Float) + cast(fails_cte.c.count, Float))
        )

        main_stmt = (
            select(winners_cte.c.user_uuid, ratio.label("ratio"))
            .join(draws_cte, winners_cte.c.user_uuid == draws_cte.c.user_uuid)
            .join(fails_cte, winners_cte.c.user_uuid == fails_cte.c.fails)
            .order_by(ratio.desc())

        )

        result_dict = {}
        count = 0
        with self.session_factory() as session:
            results = session.execute(main_stmt).all()

            for row in results:
                session.merge(Leaderboard(user_uuid=row.user_uuid, ratio=row.ratio))
                if count < n:
                    result_dict[row.user_uuid] = row.ratio
                    count += 1

            session.commit()
        return result_dict
