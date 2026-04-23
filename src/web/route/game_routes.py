from zoneinfo import available_timezones

from flask import Blueprint, jsonify, request
from di.container import container
from web.module.controller_web import ControllerWeb
from web.module.user_authenticator import UserAuthenticator
from web.model.game_web import GameWebDTO
from web.mapper.web_mapper import WebMapper

game_bp = Blueprint('game_bp', __name__)


@game_bp.route('/new_game', methods=['POST'])
@UserAuthenticator.protected
def create_game(user_uuid):
    """"Создание новой игры: с человеком или с компьютером"""
    data = request.get_json()
    game_type = data['game_type']

    new_game = GameWebDTO()
    new_game.set_uuid_player(user_uuid)
    new_game.set_game_type(game_type)

    container.game_service.add_game(WebMapper.web_to_domain(new_game))

    return jsonify({
        'message': 'Game created',
        'game_id': new_game.uuid
    })


@game_bp.route('/get_games')
@UserAuthenticator.protected
def get_games(user_uuid):
    """"Получить список всех активных игр"""
    games = container.game_service.get_active_games()
    all_games = []

    for game in games:
        all_games.append(game.uuid)

    return jsonify({f'query from user {user_uuid}, all active games': all_games})


@game_bp.route('/get_current_game')
@UserAuthenticator.protected
def get_current_game(user_uuid):
    """"Получить определенную игру"""

    data = request.get_json()
    game_uuid = data['game_uuid']
    game = container.game_service.get_current_game(game_uuid)

    return jsonify({
        'curent game:': game.uuid,
        'field:': game.field,
        'status:': game.status,
        'type:': game.type,
        'draw': game.draw,
        'winner': game.winner
    })


@game_bp.route('/make_move', methods=['POST'])
@UserAuthenticator.protected
def make_move(user_uuid):
    try:
        # from web.model.field_web import FieldWeb
        from web.model.game_web import GameWebDTO
        if not request.is_json:
            return jsonify({
                'error_1': 'Content-Type must be application/json'
            }), 415

        data = request.get_json()
        if not data:
            return jsonify({'error_2': 'No data provided'}), 400
        field = data.get('field')
        uuid_game = data.get('uuid_game')

        controller = ControllerWeb(container.game_service)
        game_web = controller.download_game(uuid_game)
        game_web.field.field = field
        game_web = controller.make_move(game_web, user_uuid)
        return jsonify({'field': game_web.field.field,
                        'game_id': str(game_web.uuid),
                        'status': game_web.status
                        })

    except Exception as e:
        print(f"Ошибка_3: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error_4': str(e)}), 500


@game_bp.route('/join', methods=['POST'])
@UserAuthenticator.protected
def join_game(user_uuid):
    controller = ControllerWeb(container.game_service)
    joined_game = controller.join_game(user_uuid)
    if joined_game:
        return jsonify({"joined game": joined_game.uuid})
    return jsonify({"Games for join": "None"})


@game_bp.route('/get_user')
@UserAuthenticator.protected
def get_user(user_uuid):
    """"Получить информацию об игроке"""

    user = container.game_service.get_user(user_uuid)

    return jsonify({
        'user uuid:': user.uuid,
        'login:': user.login,
    })
