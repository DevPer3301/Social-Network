from main import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(profile_id):
    return Profile.query.get(int(profile_id))


class Profile(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=255), nullable=False)
    email = db.Column(db.String(length=255), nullable=False)
    password_hash = db.Column(db.String(length=255), nullable=False)
    last_login = db.Column(db.DateTime(), default=datetime.utcnow)
    post = db.relationship('Post', backref='profile')

    def __repr__(self):
        return self.username

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Vote(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('profile.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    voted_at = db.Column(db.DateTime(), default=datetime.utcnow)
    vote = db.Column(db.String(length=255), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    body = db.Column(db.String(length=255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    owner_id = db.Column(db.Integer(), db.ForeignKey('profile.id'))

    def is_liked(self, user_id):
        vote = Vote.query.filter_by(user_id=user_id).filter_by(post_id=self.id).filter_by(vote="Like").first()
        if vote is not None:
            return True
        else:
            return False

    def is_disliked(self, user_id):
        vote = Vote.query.filter_by(user_id=user_id).filter_by(post_id=self.id).filter_by(vote="Dislike").first()
        if vote is not None:
            return True
        else:
            return False

    def __repr__(self):
        return self.name

