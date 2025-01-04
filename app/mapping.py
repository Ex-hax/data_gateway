from typing import Dict, Callable, Any
from config import config, base_dir
import inspect, os

print('Current Base dir:', base_dir)
init_scripts: str = os.path.join(base_dir, 'init_scripts', 'database_backend')
print('Init script folder:', init_scripts)

class submit_sql:
    @staticmethod
    def create_admin() -> Dict[str,Any]:
        from werkzeug.security import generate_password_hash
        import secrets
        admin_password: str = secrets.token_urlsafe(16)
        with open(os.path.join(base_dir,'.password'), 'w') as fs:
            fs.write(admin_password)
        admin_password_hash: str = generate_password_hash(admin_password)

        # MAIN PATTERN FOR RETURN VALUE
        return {
            'sql': os.path.join(init_scripts, 'create_admin.sql'),
            'params': {
                'password': admin_password_hash
            }
        }
    
    @staticmethod
    def set_database_timezone() -> Dict[str,Any]:
        # MAIN PATTERN FOR RETURN VALUE
        return {
            'sql': os.path.join(init_scripts, 'set_database_timezone.sql'),
            'params': {
                'database': config.SQLALCHEMY_DATABASE_URI.split('/')[-1],
                'timezone': 'UTC'
            }
        }

# Dynamically create a mapping of method names to their callable results
mapping: Dict[str, Callable] = {
    name: method() for name, method in inspect.getmembers(submit_sql, predicate=inspect.isfunction)
}