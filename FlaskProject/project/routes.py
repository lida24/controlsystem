from project import app
from flask import render_template, redirect, url_for, flash
from project.models import Item, Plant, Comptypes, Components
from project.forms import AddComponentForm, RegisterForm, LoginForm
from project import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/project')
@login_required
def project_page():
    components = Components.query.all()
    return render_template('project.html', components=components)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Plant(username=form.username.data,
                              password=form.password1.data)              
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Пользователь успешно создан! Вы вошли в систему как: {user_to_create.username}', category='success')
        return redirect(url_for('work_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Произошла ошибка регистрации пользователя: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Plant.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Успешно! Вы вошли в систему как: {attempted_user.username}', category='success')
            return redirect(url_for('work_page'))
        else:
            flash('Имя пользователя и пароль не совпадают! Попробуйте снова', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("Вы не вошли в систему!", category='info')
    return redirect(url_for("home_page"))

@app.route('/work', methods=['GET', 'POST'])
@login_required
def work_page():
    form = AddComponentForm()
    form.ctype.choices = [(comptypes.name, comptypes.decoding) for comptypes in Comptypes.query.all()]

    if form.validate_on_submit():
        component_to_create = Components(qrcode=form.qrcode.data,
                                         ctype=form.ctype.data,
                                         addts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                         cstat="new",
                                         statts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                         owner=current_user.id
                                        )              
        db.session.add(component_to_create)
        db.session.commit()
        flash(f'Деталь успешно добавлена! Продолжайте дальше', category='success')
        return redirect(url_for('work_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Произошла ошибка добавления новой детали: {err_msg}', category='danger')

    return render_template('work.html', form=form)