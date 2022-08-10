from datetime import datetime
from project import db, login_manager, admin
from project import bcrypt
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for

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
    ctype = db.Column(db.String(length=150), db.ForeignKey('comptypes.name'))
    addts = db.Column(db.DateTime(), nullable=False)
    cstat = db.Column(db.String(length=30), nullable=False, default='новый')
    statts = db.Column(db.DateTime(), nullable=False)
    tests = db.Column(db.String(length=150), default='Отсутствует')
    rem = db.Column(db.String(length=1024), default='Отсутствует')
    owner = db.Column(db.Integer(), db.ForeignKey('plant.id'))
    conclusion = db.Column(db.String(length=1024), nullable=False, default='-')
    server_id = db.Column(db.Integer(), db.ForeignKey('servers.id'))
    

class Servers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    qrcode = db.Column(db.String(length=180))
    asts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    vts = db.Column(db.DateTime, default=datetime.utcnow)
    aid = db.Column(db.Integer(), db.ForeignKey('plant.id'))
    """ vid = db.Column(db.Integer(), primary_key=True) """
    cmps = db.relationship('Components', backref='components')
    tstts = db.Column(db.DateTime, default=datetime.utcnow)
    tstres = db.Column(db.String(length=2048))
    sstat = db.Column(db.String(length=30), unique=True)
    snum = db.Column(db.String(length=30), unique=True)

class Comptypes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=150), nullable=False, unique=True)
    count = db.Column(db.Integer(), nullable=False)
    decoding = db.Column(db.String(length=150), nullable=False, unique=True)
    components = db.relationship('Components', backref='type_of_components')

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.html'))

def __repr__(self):
        return f'Item {self.name}'

admin.add_view(ModelView(Plant, db.session))
admin.add_view(ModelView(Comptypes, db.session))
admin.add_view(ModelView(Components, db.session))
admin.add_view(ModelView(Servers, db.session))