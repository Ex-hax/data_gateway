
from app.blueprints.authenticate import authenticate
from quart import request, redirect, render_template, render_template_string, url_for, flash, jsonify
from quart_auth import login_required, login_user, logout_user, current_user
from quart_cors import route_cors
from quart_schema import hide

@authenticate.route('/test', methods=['GET','POST'])
@hide
@login_required
async def test():
    headers = request.headers
    print(headers)
    print(current_user)
    return jsonify(message='Login succesful!!!')

