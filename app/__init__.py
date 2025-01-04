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
        from sqlalchemy.sql import text
        from werkzeug.security import generate_password_hash
        import secrets
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
            sql_init_scripts_folder: str = os.path.join(base_dir, 'init_scripts', 'database_backend')
            if os.path.exists(sql_init_scripts_folder):
                for file in os.listdir(sql_init_scripts_folder):
                    if file.endswith('.sql'):  # Use `.sql` instead of `.csv` for SQL scripts
                        file_path: str = os.path.join(sql_init_scripts_folder, file)
                        with open(file_path, 'r') as f:
                            sql_text: str = f.read()

                            async with app.app_context():
                                try:
                                    # Execute the SQL script
                                    print(f"Executing SQL script: {file_path}")
                                    # Generate admin password
                                    admin_password: str = secrets.token_urlsafe(16)
                                    admin_password_hash: str = generate_password_hash(admin_password)
                                    db.session.execute(text(Template(sql_text).render(params={
                                        'password': admin_password_hash
                                        # 'database_name': app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1]  # THIS LINE CAUSE ERROR TODO  change logic submit SQL job!!
                                    })))
                                    db.session.commit()
                                    print("SQL script executed successfully.")
                                    #  Write password to .password in server only knon password when see this file -> Chnage to send email ..
                                    with open(os.path.join(base_dir,'.password'), 'w') as fs:
                                        fs.write(admin_password)
                                except Exception as e:
                                    db.session.rollback()
                                    print(f"Error executing SQL script: {e}")
            else:
                print(f"SQL scripts folder not found: {sql_init_scripts_folder}")

        except Exception as e:
            print('Initialize failed some feature may not work correctly')
            print(e)

    @app.after_serving
    async def closing():
        db.session.close()
        print('\nConnection from database was closed.')

    return app

app: Quart = create_app(config)
