from app.blueprints.apis import apis
from quart import jsonify
from quart_schema import RequestSchemaValidationError

@apis.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(error):
    print(error.validation_error)
    return jsonify(errors = str(error.validation_error)), 400