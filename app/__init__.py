from config import config, base_dir
import quart_flask_patch
from quart import Quart, redirect, url_for, render_template_string, make_response, send_from_directory
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound, MethodNotAllowed, RequestTimeout, TooManyRequests, NotImplemented, InternalServerError
from jinja2 import Template

def create_app(config_object: config) -> Quart:
    
    from app.extensions import db, migrate, login_manager, schemas#, rate_limiter
    from quart_cors import cors
    import os

    # from quart_rate_limiter import limit_blueprint, rate_limit
    # from datetime import timedelta
    app: Quart = Quart(__name__, static_folder='static')
    #celery = make_celery(app)
    app.config.from_object(config_object)

    # Initialize quart extensions here
    # login_manager.login_view = 'authenticate.login'
    # import models for authenticate
    app: Quart = cors(app)
    db.init_app(app)
    migrate.init_app(app,db,compare_type=True)
    # rate_limiter.init_app(app)
    login_manager.init_app(app)

    schemas.init_app(app)

    #Custom HTTP error handler every routes
    @app.errorhandler(BadRequest)
    async def bad_request(*_):
        print('BadRequest')
        return await make_response(render_template_string('<h1>BAD REQUEST ): </h1>'), 400)
    @app.errorhandler(Unauthorized)
    async def unauthorized(*_):
        print('Unauthorized')
        return await make_response(redirect(url_for("authenticate.login")), 401)
    @app.errorhandler(Forbidden)
    async def forbidden(*_):
        print('Forbidden')
        return await make_response(render_template_string('<h1>Forbidden ): </h1>'), 403)
    @app.errorhandler(NotFound)
    async def not_found(*_):
        print('NotFound')
        return await make_response(render_template_string('<h1>NotFound ): </h1>'), 404)
    @app.errorhandler(MethodNotAllowed)
    async def method_not_allowed(*_):
        print('MethodNotAllowed')
        return await make_response(render_template_string('<h1>MethodNotAllowed ): </h1>'), 405)
    @app.errorhandler(RequestTimeout)
    async def request_timeout(*_):
        print('RequestTimeout')
        return await make_response(render_template_string('<h1>RequestTimeout ): </h1>'), 408)
    @app.errorhandler(TooManyRequests)
    async def too_many_requests(*_):
        print('TooManyRequests')
        return await make_response(render_template_string('<h1>TooManyRequests ): </h1>'), 429)
    @app.errorhandler(InternalServerError)
    async def internal_server_error(*_):
        print('InternalServerError')
        return await make_response(render_template_string('<h1>InternalServerError ): </h1>'), 500)
    @app.errorhandler(NotImplemented)
    async def not_implemented(*_):
        print('NotImplemented')
        return await make_response(render_template_string('<h1>NotImplemented ): </h1>'), 501)

    # Register blueprints here
    from app.blueprints.authenticate import authenticate as authenticate
    app.register_blueprint(authenticate,url_prefix='/authenticate')
    # limit_blueprint(compoxer, 5, timedelta(seconds=1))

    from app.blueprints.apis import apis as apis
    app.register_blueprint(apis,url_prefix='/apis')
    # limit_blueprint(compoxer, 5, timedelta(seconds=1))

    @app.route('/favicon.ico')
    async def favicon():
        return await send_from_directory(os.path.join(app.root_path, 'static/res/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.before_serving
    async def initialize():
        from app.mapping import mapping
        from sqlalchemy.sql import text
        try:
            migrate_folders: str = os.path.join(base_dir, 'migrations')
            is_migration_folder: bool = os.path.exists(migrate_folders)
            print(f'Migrations folder found is {is_migration_folder}')
            # Always found according to mount volume in docker-compose for contain migrations folder data with relate to alembic table in database
            if is_migration_folder and not os.listdir(migrate_folders): 
                os.system('quart db init')
                os.system('quart db migrate')
                os.system('quart db upgrade')
            else:
                os.system('quart db migrate')
                os.system('quart db upgrade')

            # Execute SQL scripts from the 'init_scripts/database_backend' folder
            async with app.app_context():
                for _ , value in mapping.items():
                    try:
                        # Read sql
                        print('\n--------------------------------------------------')
                        print(value['sql'])
                        with open(value['sql'], 'r') as f:
                            sql_text: str = f.read()
                        # Execute the SQL script
                        print(f"Executing SQL script: {value['sql']}")
                        sql_text: text = text(Template(sql_text).render(params=value['params']))
                        print(sql_text)
                        db.session.execute(sql_text)
                        db.session.commit()
                        print("SQL script executed successfully.")
                        print('--------------------------------------------------\n')

                    except Exception as e:
                        db.session.rollback()
                        print(f"Error executing SQL script: {e}")
                        print('--------------------------------------------------\n')

        except Exception as e:
            print('Initialize failed some feature may not work correctly')
            print(e)

    @app.after_serving
    async def closing():
        db.session.close()
        print('\nConnection from database was closed.')

    return app

app: Quart = create_app(config)
