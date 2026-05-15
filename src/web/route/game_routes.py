from flask import Blueprint, jsonify, request
from di.container import container
from web.module.controller_web import ControllerWeb
from web.module.user_authenticator import UserAuthenticator
from web.model.game_web import GameWebDTO
from flask_jwt_extended import jwt_required, get_jwt_identity

game_bp = Blueprint('game_bp', __name__)


@game_bp.route('/new_game', methods=['POST'])
# @UserAuthenticator.protected
@jwt_required()
def create_game():
    """"Создание новой игры: с человеком или с компьютером"""
    try:
        print("==========creating game...")
        data = request.get_json()
        if not data or 'game_type' not in data:
            return jsonify({'error': 'Missing game_type in request'}), 400

        game_type = data['game_type']
        new_game = GameWebDTO()
        user_uuid = get_jwt_identity()
        new_game.set_uuid_player(user_uuid)
        new_game.set_game_type(game_type)

        controller = ControllerWeb(container.game_service)
        new_game = controller.create_game(new_game)
        if not new_game:
            return jsonify({'error': 'Cant create new game'}), 400

        return jsonify({
            'status': new_game.status,
            'game_id': new_game.uuid
        })
    except Exception as e:
        print(f"Error in create new game: {e}")
        return jsonify({'error': 'Internal server error during game creation'}), 500


@game_bp.route('/get_games')
# @UserAuthenticator.protected
@jwt_required()
def get_games():
    """"Получить список всех активных игр"""
    try:
        games = container.game_service.get_active_games()
        all_games = []

        for game in games:
            all_games.append(game.uuid)
        user_uuid = get_jwt_identity()
        return jsonify({f'query from user {user_uuid}, all active games': all_games})
    except Exception as e:
        print(f"Error in get_games: {e}")
        return jsonify({'error': 'Internal server error while fetching games'}), 500


@game_bp.route('/get_current_game')
# @UserAuthenticator.protected
@jwt_required()
def get_current_game():
    """"Получить определенную игру"""
    try:
        data = request.get_json()
        if not data or 'game_uuid' not in data:
            return jsonify({'error': 'Missing game_uuid in request'}), 400
        game_uuid = data['game_uuid']
        game = container.game_service.get_current_game(game_uuid)
        if game is None:
            return jsonify({'error': 'Game not found'}), 404
        return jsonify({
            'current game:': game.uuid,
            'field:': game.field,
            'status:': game.status,
            'type:': game.type,
            'draw': game.draw,
            'winner': game.winner
        })
    except Exception as e:
        print(f"Error in get_current_game: {e}")
        return jsonify({'error': 'Internal server error while fetching current games'}), 500


@game_bp.route('/make_move', methods=['POST'])
# @UserAuthenticator.protected
@jwt_required()
def make_move():
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
        if not field or not uuid_game:
            return jsonify({'error': 'Missing field or uuid_game in request'}), 400
        controller = ControllerWeb(container.game_service)
        game_web = controller.download_game(uuid_game)
        game_web.field.field = field
        user_uuid = get_jwt_identity()
        game_web = controller.make_move(game_web, user_uuid)
        if game_web is None:
            return jsonify({'error': 'Game not found or not valid field'}), 404
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
# @UserAuthenticator.protected
@jwt_required()
def join_game():
    try:
        controller = ControllerWeb(container.game_service)
        user_uuid = get_jwt_identity()
        joined_game = controller.join_game(user_uuid)
        if joined_game:
            return jsonify({"player": user_uuid, "joined to game": joined_game.uuid})
        else:
            return jsonify({"message": "No available games to join"}), 404
    except Exception as e:
        print(f"Error in join game: {e}")
        return jsonify({'Error': 'Internal server error while joining game'}), 500


@game_bp.route('/get_user')
@UserAuthenticator.protected
@jwt_required()
def get_user():
    """"Получить информацию об игроке"""
    try:
        user_uuid = get_jwt_identity()
        user = container.game_service.get_user(user_uuid)
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user uuid:': user.uuid,
            'login:': user.login,
        })
    except Exception as e:
        print(f"Error in get_user: {e}")
        return jsonify({'error': 'Internal server error while fetching user info'}), 500
