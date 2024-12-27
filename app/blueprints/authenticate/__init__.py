from quart import Blueprint
from quart_cors import cors

authenticate: Blueprint = Blueprint('authenticate', __name__,template_folder='templates',static_folder='static')
authenticate: Blueprint = cors(authenticate)

from app.blueprints.authenticate import routes, views, error_handle
from app.blueprints.authenticate.models.user import user
from app.blueprints.authenticate.models.login_log import login_log
