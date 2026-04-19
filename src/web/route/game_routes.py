from flask import Blueprint, jsonify, request
from uuid import UUID, uuid4
from flask_reqcheck import validate_body, get_valid_request
from domain.model.game import CurrentGame
from di.container import container
from web.module.controller_web import ControllerWeb
from datasource.database.sign_up_request import SignUpRequest
import base64
from web.module.user_authenticator import UserAuthenticator
from datasource.database.database import Games
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

    container.user_bd_service.save_game(WebMapper.from_web_to_db(new_game))



    return jsonify({
        'message': 'Game created',
        'game_id': new_game.uuid
    })


# @game_bp.route('/<user_name>')
# @UserAuthenticator.protected
# def new_game(user_name):
#     game = CurrentGame()
#     game.set_user_name(user_name)
#
#     game.user_info.hashed_password = "tratata"  # NB!!!!
#     # container.game_service.repository.save(game)
#     container.user_repository.save(game.user_info)
#
#     return jsonify({
#         'message': 'New Game created',
#         'user_name': user_name,
#         'game_id': str(game.UUID),
#         'field': game.field.field
#     })


# @game_bp.route('/get_game/<game_id>')
# def get_game(game_id):
#     game_uuid = UUID(game_id)
#
#     game = container.game_service.repository.get(game_uuid)
#
#     return jsonify({'field': game.field.field,
#                     'game_id': str(game.UUID),
#                     'message': 'Game loaded'})


@game_bp.route('/make_move/<game_id>', methods=['POST'])
@UserAuthenticator.protected
def make_move(game_id):
    try:
        from web.model.field_web import FieldWeb
        from web.model.game_web import GameWebDTO
        if not request.is_json:
            return jsonify({
                'error_1': 'Content-Type must be application/json'
            }), 415

        data = request.get_json()
        if not data:
            return jsonify({'error_2': 'No data provided'}), 400
        field = data.get('field')
        game_field = FieldWeb()
        game_field.field = field
        game_web = GameWebDTO(game_id, game_field)
        controller = ControllerWeb(container.game_service)
        game_web = controller.make_move(game_web)
        return jsonify({'field': game_web.field.field,
                        'game_id': str(game_web.uuid),
                        'message': 'Game changed'})

    except Exception as e:
        print(f"Ошибка_3: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error_4': str(e)}), 500
