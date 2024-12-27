from quart import Blueprint
from quart_cors import cors

apis: Blueprint = Blueprint('apis', __name__,template_folder='templates',static_folder='static')
apis: Blueprint = cors(apis, **{'allow_origin': '*'})

from app.blueprints.apis import routes, error_handle

