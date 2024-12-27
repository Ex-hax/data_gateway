from itsdangerous import BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer
from quart import Quart, current_app, jsonify, request, make_response
from quart_auth.extension import _get_config_or_default
from datetime import timedelta
from typing import Dict
from functools import wraps
from app.blueprints.authenticate.models.user import user


class token_bearer:
    def __init__(self, app: Quart | None = None):
        self.app = app if app is not None else current_app
        self.serializer = URLSafeTimedSerializer(
            self.app.secret_key,
            _get_config_or_default("QUART_AUTH_SALT", self.app),
        )

    def generate_bearer_token(self, user_uuid: str):
        return self.serializer.dumps(user_uuid)
    
    def verify_bearer_token(self, bearer_token: str, expired_duration: timedelta | float | int | None = None):
        return self.serializer.loads(bearer_token, max_age=expired_duration if not None else _get_config_or_default("QUART_AUTH_DURATION", self.app))
    

def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[-1]

        if not token:
            print('Token is missing !!')
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            api_current_user = user.query.filter_by(uuid = token_bearer().verify_bearer_token(bearer_token=token)).first()
        except SignatureExpired:
            print('An expired token was used.')
            return await make_response(jsonify({
                'message' : 'An expired token was used.'
            }), 400)
        except BadSignature:
            print('Bad signature detected.')
            return await make_response(jsonify({
                'message' : 'Bad signature detected.'
            }), 400)

        return await current_app.ensure_async(f)(api_current_user, *args,**kwargs)

    return decorated