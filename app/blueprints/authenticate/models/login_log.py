from app.extensions import db
from sqlalchemy.dialects.postgresql import TIMESTAMP, ENUM
import pendulum

class login_types:
    COOKIE: str = 'cookie'
    BEARER: str = 'bearer'
    _LOGIN_TYPE_ENUM: ENUM = ENUM(COOKIE, BEARER, name='login_type_enum', create_type=True)
    _valid_types = {COOKIE, BEARER}

    @classmethod
    def check(cls, login_type: str) -> str:
        """
        Validates if the provided login_type is valid. If valid, it returns the login_type.
        If invalid, it raises a ValueError.
        """
        if login_type in cls._valid_types:
            return login_type
        raise ValueError(f"Invalid login type: {login_type}. Valid options are: {', '.join(cls._valid_types)}")

    def __getattr__(self, item: str) -> str:
        """
        Dynamically checks for valid attributes corresponding to login types.
        Raises an AttributeError for invalid attributes.
        """
        if item.upper() in {'COOKIE', 'BEARER'}:
            return getattr(self, item.upper())
        raise AttributeError(f"{item} is not a valid login type. Use one of: {', '.join(self._valid_types)}")

    def __init__(self):
        raise NotImplementedError("LoginType is a static class and should not be instantiated.")

class login_log(db.Model):
    __tablename__ = 'login_log'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    login_type = db.Column(login_types._LOGIN_TYPE_ENUM, nullable=False)
    logged_in_datetime = db.Column(TIMESTAMP(timezone=True), nullable=False)

    def __init__(self, user_id: int, login_type: str, logged_in_datetime: None = None) -> None:
        self.user_id: int = user_id
        self.login_type: str = login_types.check(login_type)
        self.logged_in_datetime: pendulum = logged_in_datetime or pendulum.now('UTC')

    def __repr__(self) -> str:
        return f'id:{self.id}, user_id:{self.user_id}, login_type:{self.login_type}, logged_in_datetime:{self.logged_in_datetime}\n'