from app.extensions import db
# from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from quart_auth import AuthUser

class user(db.Model, AuthUser):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    user_name = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    mobile_phone = db.Column(db.String(), nullable=False, unique=True)
    #is_active = db.Column(db.Boolean(),nullable=False)

    def __init__(self,uuid,user_name,password,email,mobile_phone) -> None:
        self.uuid = uuid
        self.user_name = user_name
        self.password = generate_password_hash(password)
        self.email = email
        self.mobile_phone = mobile_phone
        #self.is_active = is_active
        
    def verify_password(self,pwd) -> bool:
        return check_password_hash(self.password,pwd)

    @staticmethod
    def generate_password(password) -> str:
        return generate_password_hash(password)

    def __repr__(self) -> str:
        return f'id:{self.id}, uuid:{self.uuid}, name:{self.user_name}, email:{self.email}, password:{self.password}, mobile_phone:{self.mobile_phone}\n'

class LoginForms(FlaskForm):
    user_name = StringField('Username',validators=[DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')