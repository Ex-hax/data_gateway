from app.blueprints.authenticate import authenticate
from quart import jsonify
from quart_schema import RequestSchemaValidationError

@authenticate.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(error):
    print(error.validation_error)
    return jsonify(errors = str(error.validation_error)), 400