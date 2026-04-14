from flask import Blueprint, jsonify, request
from uuid import UUID
from flask_reqcheck import validate_body, get_valid_request
from domain.model.game import CurrentGame
from di.container import container
from web.module.controller_web import ControllerWeb
from datasource.database.sign_up_request import SignUpRequest
import base64

game_bp = Blueprint('game', __name__)


def decode_base(header: str):
    if not header or not header.startswith('Basic '):
        return None, None
    try:
        encoded = header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        login, password = decoded.split(':', 1)
        return login, password
    except Exception:
        return None, None


@game_bp.route('/register', methods=['POST'])
@validate_body(SignUpRequest)
def register_user():
    validated_request = get_valid_request()
    success = container.user_service.register(validated_request.body)
    if success:
        return {"message": f"{validated_request.body.login} was successful registered"}, 201
    else:
        return {"error": "Login exists"}, 409


@game_bp.route('/authorize', methods=['POST'])
def authorize_user():
    auth_header = request.headers.get('Authorization')
    login, password = decode_base(auth_header)
    if not login or not password:
        return jsonify({"error": "Invalid or missing Basic Auth header"}), 401

    user_uuid = container.user_service.authorize(login, password)
    if user_uuid is None:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"user_uuid": user_uuid}), 200


@game_bp.route('/create_game')
def create_game():
    game = CurrentGame()
    container.game_service.repository.save(game)

    return jsonify({
        'message': 'Game created',
        'game_id': str(game.UUID),
        'field': game.field.field
    })


@game_bp.route('/<user_name>')
def new_game(user_name):
    game = CurrentGame()
    game.set_user_name(user_name)

    game.user_info.hashed_password = "tratata"  # NB!!!!
    # container.game_service.repository.save(game)
    container.user_repository.save(game.user_info)

    return jsonify({
        'message': 'New Game created',
        'user_name': user_name,
        'game_id': str(game.UUID),
        'field': game.field.field
    })


@game_bp.route('/get_game/<game_id>')
def get_game(game_id):
    game_uuid = UUID(game_id)

    game = container.game_service.repository.get(game_uuid)

    return jsonify({'field': game.field.field,
                    'game_id': str(game.UUID),
                    'message': 'Game loaded'})


@game_bp.route('/make_move/<game_id>', methods=['POST'])
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
        # game_uuid = UUID(game_id)
        game_web = GameWebDTO(game_id, game_field)
        # print("========================")
        # print(f"Получено поле из запроса: {data['field']}")
        # print("========================")
        controller = ControllerWeb(container.game_service)
        game_web = controller.make_move(game_web)
        # print(f"измененное поле {game_web.field.field}")
        return jsonify({'field': game_web.field.field,
                        'game_id': str(game_web.uuid),
                        'message': 'Game changed'})

    except Exception as e:
        print(f"Ошибка_3: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error_4': str(e)}), 500
