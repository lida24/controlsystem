from crypt import methods
from wsgiref.simple_server import server_version
from project import app
from flask import render_template, redirect, url_for, flash, request
from project.models import Item, Plant, Comptypes, Components, Servers
from project.forms import AddComponentForm, RegisterForm, LoginForm, PowerSupplyTestingForm, PowerManagementModuleTestingForm, HandleTestingForm, ComponentSearchForm
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
        return redirect(url_for('add_component_page'))
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
            return redirect(url_for('add_component_page'))
        else:
            flash('Имя пользователя и пароль не совпадают! Попробуйте снова', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("Вы не вошли в систему!", category='info')
    return redirect(url_for("home_page"))

@app.route('/select_action')
@login_required
def select_action_page():
    return render_template('select_action.html')

@app.route('/all_components')
def all_components_page():
    components = Comptypes.query.all()
    return render_template('all_components.html', components=components)

@app.route('/all_servers')
def all_servers_page():
    servers = Servers.query.all()
    return render_template('all_servers.html', servers=servers)

@app.route('/<int:component_id>/')
def current_component_page(component_id):
    comptypes = Comptypes.query.get_or_404(component_id)
    return render_template('current_component.html', comptypes=comptypes)

@app.route('/add_component', methods=['GET', 'POST'])
@login_required
def add_component_page():
    form = AddComponentForm()
    form.ctype.choices = [(comptypes.name, comptypes.decoding) for comptypes in Comptypes.query.all()]

    if form.validate_on_submit():
        component_to_create = Components(qrcode=form.qrcode.data,
                                         ctype=form.ctype.data,
                                         addts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                         statts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                         owner=current_user.id
                                        )       
        db.session.add(component_to_create)
        comptypes = Comptypes.query.filter_by(name=form.ctype.data).first()
        comptypes.count = comptypes.count + 1
        db.session.add(comptypes)
        db.session.commit()
        flash(f'Деталь успешно добавлена! Продолжайте дальше', category='success')
        return redirect(url_for('add_component_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Произошла ошибка добавления новой детали: {err_msg}', category='danger')

    return render_template('add_component.html', form=form)

@app.route('/add_chassis', methods=['GET', 'POST'])
def add_chassis_page():
    form = ComponentSearchForm()
    
    if form.validate_on_submit():
        result = Components.query.filter_by(qrcode=form.search.data).first()
        if result.ctype == 'chassis' and result.cstat == 'протестирован' and result.conclusion == 'Годен':
            server_to_create = Servers(qrcode=result.qrcode,
                                       asts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                       aid=current_user.id,
                                       cmps=[result]
                                      )
            result.cstat = 'установлен в изделие'
            db.session.add(server_to_create)
            db.session.add(result)
            db.session.commit()
            count = 1
            flash(f'Деталь успешно добавлена в сервер! Продолжайте дальше', category='success')
            return redirect(url_for('add_fan_140_page', server_id=server_to_create.id, count=count))
        elif result.cstat == 'забракован':
            flash('Компонент числится, как забракованный', category='danger')
        elif result.ctype != 'chassis':
            flash('Вы отсканировали другую деталь, пожалуйста отсканируйте корпус сервера СХД!', category='danger')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Произошла ошибка добавления новой детали в сервер: {err_msg}', category='danger')

    return render_template('add_chassis.html', form=form)

@app.route('/add_fan_140/<int:server_id>/<int:count>', methods=['GET', 'POST'])
def add_fan_140_page(server_id, count):
    form = ComponentSearchForm()
    server = Servers.query.filter_by(id=server_id).first()
    if form.validate_on_submit():
        result = Components.query.filter_by(qrcode=form.search.data).first()
        if result.ctype == 'fan_140' and result.cstat == 'протестирован' and result.conclusion == 'Годен':
            server.cmps += [result]
            result.cstat = 'установлен в изделие'
            db.session.add(server)
            db.session.add(result)
            db.session.commit()
            if count < 3:
                count += 1
                flash(f'Деталь успешно добавлена в сервер! Продолжайте дальше', category='success')
                return redirect(url_for('add_fan_140_page', server_id=server_id, count=count))
            else:
                return redirect(url_for('add_fan_control_board_page', server_id=server_id))
    return render_template('add_fan_140.html', form=form, count=count)

@app.route('/add_fan_control_board/<int:server_id>', methods=['GET', 'POST'])
def add_fan_control_board_page(server_id):
    form = ComponentSearchForm()
    server = Servers.query.filter_by(id=server_id).first()
    if form.validate_on_submit():
        result = Components.query.filter_by(qrcode=form.search.data).first()
        if result.ctype == 'fan_control_board' and result.cstat == 'протестирован' and result.conclusion == 'Годен':
            server.cmps += [result]
            result.cstat = 'установлен в изделие'
            db.session.add(server)
            db.session.add(result)
            db.session.commit()
            count = 1
            flash(f'Деталь успешно добавлена в сервер! Продолжайте дальше', category='success')
            return redirect(url_for('add_fan_40_page', server_id=server_id, count=count))
    return render_template('add_fan_control_board.html', form=form)

@app.route('/add_fan_40/<int:server_id>/<int:count>', methods=['GET', 'POST'])
def add_fan_40_page(server_id, count):
    form = ComponentSearchForm()
    server = Servers.query.filter_by(id=server_id).first()
    if form.validate_on_submit():
        result = Components.query.filter_by(qrcode=form.search.data).first()
        if result.ctype == 'fan_40' and result.cstat == 'протестирован' and result.conclusion == 'Годен':
            server.cmps += [result]
            result.cstat = 'установлен в изделие'
            db.session.add(server)
            db.session.add(result)
            db.session.commit()
            if count < 6:
                count += 1
                flash(f'Деталь успешно добавлена в сервер! Продолжайте дальше', category='success')
                return redirect(url_for('add_fan_40_page', server_id=server_id, count=count))
            else:
                return redirect(url_for('add_indicator_board_page', server_id=server_id))
    return render_template('add_fan_40.html', form=form, count=count)

@app.route('/add_indicator_board/<int:server_id>/', methods=['GET', 'POST'])
def add_indicator_board_page(server_id):
    form = ComponentSearchForm()
    server = Servers.query.filter_by(id=server_id).first()
    if form.validate_on_submit():
        result = Components.query.filter_by(qrcode=form.search.data).first()
        if result.ctype == 'indicator_board' and result.cstat == 'протестирован' and result.conclusion == 'Годен':
            server.cmps += [result]
            result.cstat = 'установлен в изделие'
            db.session.add(server)
            db.session.add(result)
            db.session.commit()
            flash(f'Деталь успешно добавлена в сервер! Продолжайте дальше', category='success')
            return redirect(url_for('add_power_management_module_page', server_id=server_id))
    return render_template('add_indicator_board.html', form=form)

@app.route('/add_power_management_module/<int:server_id>/', methods=['GET', 'POST'])
def add_power_management_module_page(server_id):
    form = ComponentSearchForm()
    server = Servers.query.filter_by(id=server_id).first()
    if form.validate_on_submit():
        result = Components.query.filter_by(qrcode=form.search.data).first()
        if result.ctype == 'power_management_module' and result.cstat == 'протестирован' and result.conclusion == 'Годен':
            server.cmps += [result]
            result.cstat = 'установлен в изделие'
            db.session.add(server)
            db.session.add(result)
            db.session.commit()
            flash(f'Деталь успешно добавлена в сервер! Продолжайте дальше', category='success')
            return redirect(url_for('add_power_management_module_page', server_id=server_id))
    return render_template('add_power_management_module.html', form=form)

@app.route('/search_results/<results>/')
def search_results_page(results):
    return render_template('search_results.html', results=results)

@app.route('/components')
def components_page():
    components = Components.query.all()
    return render_template('components.html', components=components)

@app.route('/testing/<int:component_id>/', methods=['GET', 'POST'])
def testing_page(component_id):
    component = Components.query.get_or_404(component_id)
    if component.ctype == 'power_supply_2k6':
        form = PowerSupplyTestingForm()

        if form.validate_on_submit():
            component.tests = url_for('test_results_page', component_id=component.id, component_p=[form.p.data])
            component.statts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if 11.4 <= form.p.data <= 12.6:
                component.conclusion = 'Годен'
                component.cstat = 'протестирован'
            else:
                component.conclusion = 'Не годен'
                component.cstat = 'забракован'
            db.session.add(component)
            db.session.commit()
            flash(f'Деталь успешно протестирована! Продолжайте дальше', category='success')
            comptypes = Comptypes.query.filter_by(name=component.ctype).first()
            return redirect(url_for('current_component_page', component_id=comptypes.id))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Произошла ошибка тестирования детали: {err_msg}', category='danger')

    elif component.ctype == 'power_management_module':
        form = PowerManagementModuleTestingForm()

        if form.validate_on_submit():
            component.statts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            component.tests = url_for('test_results_page', component_id=component.id, component_p=[form.p1.data, form.p2.data, form.p3.data])
            component.rem = url_for('comment_page', component_id=component.id)
            if 4.75 <= form.p1.data <= 5.25 and 3.135 <= form.p2.data <= 3.465 and 4.75 <= form.p3.data <= 5.25:
                component.conclusion = 'Годен'
                component.cstat = 'протестирован'
            else:
                component.conclusion = 'Не годен'
                component.cstat = 'забракован'
            db.session.add(component)
            db.session.commit()
            flash(f'Деталь успешно протестирована! Продолжайте дальше', category='success')
            comptypes = Comptypes.query.filter_by(name=component.ctype).first()
            return redirect(url_for('current_component_page', component_id=comptypes.id))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Произошла ошибка тестирования детали: {err_msg}', category='danger')

    elif component.ctype == 'fan_140' or component.ctype == 'fan_40' or component.ctype == 'chassis' or component.ctype == 'indicator_board' or component.ctype == 'fan_control_board':
        form = HandleTestingForm()
        if form.validate_on_submit():
            component.statts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            component.rem = url_for('comment_page', component_id=component.id)
            if request.form['action'] == 'Годен':
                component.conclusion = 'Годен'
                component.cstat = 'протестирован'
            elif request.form['action'] == 'Не годен':
                component.conclusion = 'Не годен'
                component.cstat = 'забракован'
            db.session.add(component)
            db.session.commit()
            flash(f'Деталь успешно протестирована! Продолжайте дальше', category='success')
            comptypes = Comptypes.query.filter_by(name=component.ctype).first()
            return redirect(url_for('current_component_page', component_id=comptypes.id))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Произошла ошибка тестирования детали: {err_msg}', category='danger')

    return render_template('testing.html', form=form, component=component)

@app.route('/test_results/<component_p>/')
def test_results_page(component_p):
    op = component_p.strip('][').split(', ')
    return render_template('test_results.html', component=op)

@app.route('/comment')
def comment_page():
    return render_template('comment.html')