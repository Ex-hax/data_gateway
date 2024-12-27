from quart_auth import QuartAuth
login_manager: QuartAuth = QuartAuth()

from flask_sqlalchemy import SQLAlchemy
db: SQLAlchemy = SQLAlchemy()

from flask_migrate import Migrate
migrate: Migrate = Migrate(compare_type=True)

from quart_schema import QuartSchema
schemas: QuartSchema = QuartSchema()

# from quart_db import QuartDB
# db: QuartDB = QuartDB()

# from quart_rate_limiter import RateLimiter
# from quart_rate_limiter.redis_store import RedisStore
# from config import ConfigHypercorn as cfg
# redis_store = RedisStore(cfg.REDIS_STORE)
# rate_limiter = RateLimiter(store=redis_store)