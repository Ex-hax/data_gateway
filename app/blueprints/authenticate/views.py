
from app.blueprints.authenticate import authenticate
from quart import request, redirect, render_template, render_template_string, url_for, flash, session
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
    return await render_template_string("<div class='container'>PASS</div>")

