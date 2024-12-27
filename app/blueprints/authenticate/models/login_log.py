from app.extensions import db
class login_log(db.Model):
    __tablename__ = 'login_log'
    id = db.Column(db.Integer(), primary_key=True)

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'id:{self.id},\n'