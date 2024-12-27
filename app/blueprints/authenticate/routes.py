from app.blueprints.authenticate import authenticate
from app.blueprints.authenticate.models.user import user, LoginForms
from app.blueprints.authenticate.dataclass_models.login import api_login_user
from app.blueprints.authenticate.origin_policies import login_logout_level
from app.blueprints.authenticate.modules.token_management import token_bearer, token_required
from quart import request, redirect, render_template, abort, url_for, flash, current_app, make_response, jsonify
from quart_auth import login_required, login_user, logout_user, current_user, AuthUser
from quart_cors import route_cors
from quart_schema import hide, validate_request
from werkzeug.security import check_password_hash

from datetime import datetime, timedelta

#Login cookie
@authenticate.route('/login', methods=['POST', 'GET'])
@hide
@route_cors(**login_logout_level.setting)
async def login():
    if request.method == 'POST':
        form = LoginForms(await request.form)
        if request.method == 'POST' and form.validate():
            _user = user.query.filter_by(user_name=form.user_name.data.lower()).first()
            if _user and _user.verify_password(form.password.data):
                print('Password verify is ', _user.verify_password(form.password.data))
                login_user(AuthUser(_user.id))
                if not request.args.get('next'):
                    return redirect(url_for('authenticate.test'))
                else:
                    return redirect(request.args.get('next'))
            await flash('Invalid username or password.')
            return redirect(url_for('authenticate.login'))
    if request.method == 'GET':
        form = LoginForms()
        return await render_template('/login.html', form=form)

@authenticate.route('/logout', methods=['GET'])
@hide
@route_cors(**login_logout_level.setting)
@login_required
async def logout():
    logout_user()
    return redirect(url_for('authenticate.login'))

#Login Bearer TODO recheck cross origin
@authenticate.route('/api/login', methods =['POST'])
@route_cors(allow_origin='*')
@validate_request(api_login_user)
async def api_login(data: api_login_user):
    auth = await request.get_json()
  
    if not auth or not auth['user_name'] or not auth['password']:
        return await make_response(
            jsonify(message='user_name or password not provide.'),
            400
        )
  
    _user = user.query.filter_by(user_name = auth['user_name']).first()
  
    if not _user:
        return await make_response(
            jsonify(message=f'Could not find user {auth["user_name"]}'),
            404
        )
  
    if check_password_hash(_user.password, auth['password']):
        serializer = token_bearer(app=current_app)
        token = serializer.generate_bearer_token(user_uuid=_user.uuid)
        return await make_response(jsonify({'token' : token}), 201)

    return await make_response(
        jsonify(messeage=f'Could not verify {_user.user_name}'),
        403
    )
