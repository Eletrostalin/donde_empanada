from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from .models import db, User, Location
from .forms import RegistrationForm, LoginForm, LocationForm
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    locations = Location.query.all()
    form = RegistrationForm()  # Добавление пустой формы для CSRF токена
    return render_template('index.html', locations=locations, form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user_by_username = User.query.filter_by(username=form.username.data).first()
        existing_user_by_phone = User.query.filter_by(phone_hash=form.phone.data).first()

        if existing_user_by_username:
            flash('Пользователь с таким именем уже существует. 🚫', 'danger')
            return jsonify(success=False, message='Пользователь с таким именем уже существует. 🚫')

        if existing_user_by_phone:
            flash('Пользователь с таким телефоном уже существует. 🚫', 'danger')
            return jsonify(success=False, message='Пользователь с таким телефоном уже существует. 🚫')

        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            second_name=form.second_name.data,
        )
        user.set_password(form.password.data)
        user.set_phone(form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! 😊', 'success')
        return jsonify(success=True)
    else:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        flash(f'Ошибка регистрации: {", ".join(error_messages)} 🚫', 'danger')
        app.logger.debug(f'Ошибка валидации формы: {form.errors}')
        return jsonify(success=False, message=", ".join(error_messages))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вход выполнен успешно! 😊', 'success')
            return jsonify(success=True)
        else:
            flash('Ошибка входа. Проверьте имя пользователя и пароль. 🚫', 'danger')
            return jsonify(success=False, message='Ошибка входа. Проверьте имя пользователя и пароль.')
    else:
        if request.method == 'POST':
            error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
            flash(f'Ошибки валидации формы: {", ".join(error_messages)} 🚫', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы! 😊', 'success')
    return redirect(url_for('main.index'))

@bp.route('/add_location', methods=['POST'])
@login_required
def add_location():
    app.logger.debug('Получен запрос на добавление метки')
    form = LocationForm()
    if form.validate_on_submit():
        app.logger.debug('Форма прошла валидацию')
        try:
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            app.logger.debug('Координаты: %s, %s', latitude, longitude)
            new_location = Location(
                name=form.name.data,
                description=form.description.data,
                address=form.address.data,
                working_hours=form.working_hours.data,
                average_check=form.average_check.data,
                latitude=latitude,
                longitude=longitude,
                created_by=current_user.id
            )
            db.session.add(new_location)
            db.session.commit()
            app.logger.debug('Метка успешно добавлена в базу данных')
            return jsonify(success=True)
        except Exception as e:
            app.logger.error('Ошибка при добавлении метки: %s', e)
            return jsonify(success=False, message=f'Произошла ошибка при добавлении метки: {e} 🚫')
    else:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        app.logger.debug('Ошибка валидации формы: %s', form.errors)
        return jsonify(success=False, message=f'Ошибки валидации формы: {", ".join(error_messages)} 🚫')

@bp.route('/markers')
def markers():
    locations = Location.query.all()
    markers = []
    for location in locations:
        markers.append({
            'name': location.name,
            'description': location.description,
            'latitude': location.latitude,
            'longitude': location.longitude
        })
    return jsonify(markers)
