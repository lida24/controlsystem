from datetime import datetime
from project import db, login_manager
from project import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Plant.query.get(int(user_id))

class Plant(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    components = db.relationship('Components', backref='plant_components', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    qrcode = db.Column(db.String(length=30), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('plant.id'))

class Components(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    qrcode = db.Column(db.String(length=180), nullable=False, unique=True)
    ctype = db.Column(db.String(length=1024), nullable=False)
    addts = db.Column(db.DateTime(), nullable=False)
    cstat = db.Column(db.String(length=30), nullable=False)
    statts = db.Column(db.DateTime(), nullable=False)
    tests = db.Column(db.String(length=30), default='No tests yet')
    rem = db.Column(db.String(length=1024), default='No remark yet')
    owner = db.Column(db.Integer(), db.ForeignKey('plant.id'))

class Servers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    qrcode = db.Column(db.String(length=180), nullable=False, unique=True)
    asts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    vts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    aid = db.Column(db.Integer(), primary_key=True)
    vid = db.Column(db.Integer(), primary_key=True)
    #cmps = db.Column(MutableList.as_mutable(ARRAY(db.Integer)))
    tstts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tstres = db.Column(db.String(length=2048), nullable=False)
    sstat = db.Column(db.String(length=30), nullable=False, unique=True)
    snum = db.Column(db.String(length=30), nullable=False, unique=True)

class Comptypes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=150), nullable=False, unique=True)
    decoding = db.Column(db.String(length=150), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'
