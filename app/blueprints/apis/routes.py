from app.blueprints.apis import apis
from app.blueprints.apis.origin_policies import test_route_level
from app.blueprints.apis.dataclass_models.test import test_api
from app.blueprints.authenticate.modules.token_management import token_required
from app.blueprints.authenticate.models.user import user
from quart import make_response, jsonify, request
from quart_cors import route_cors
from quart_schema import validate_request, validate_response

@apis.route('/test', methods=['POST'])
@route_cors(**test_route_level.setting)
@token_required
@validate_request(test_api)
async def test_route(api_current_user: user, data: test_api):
    print('API user', api_current_user)
    print('Data class', data)
    return jsonify(message='api_test_route data was accept.'), 200
