from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

#User table
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)

    anime_list = db.relationship('Anime',backref='user',lazy=True)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    

class Anime(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    episodes = db.Column(db.Integer)
    status = db.Column(db.String(20),nullable=False)
    source = db.Column(db.String(100))
    watch_status = db.Column(db.String(20), nullable=False, default="Plan to Watch")  # 🆕 added
    rating = db.Column(db.Float)
    link = (db.String(300))

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
