from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db
from app import login
from hashlib import md5

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	major = db.Column(db.String(64), default='')
	listings = db.relationship('Listing', backref='owner', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	def __repr__(self):
		return '<User {}>'.format(self.email)

class Listing(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(64))
	body = db.Column(db.String(1024))
	desired_size = db.Column(db.Integer, default=2) 
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	is_complete = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return '<Listing {}>'.format(self.title)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))
