from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .models import db, User, Location
from .forms import RegistrationForm, LoginForm, LocationForm
from werkzeug.security import generate_password_hash, check_password_hash
import logging

bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG)

@bp.route('/')
def index():
    locations = Location.query.all()
    form = RegistrationForm()  # Добавление пустой формы для CSRF токена
    return render_template('index.html', locations=locations, form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
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
        flash(f'Ошибка регистрации: {form.errors}', 'danger')
        logging.debug(f'Form validation failed: {form.errors}')
        return jsonify(success=False, message=form.errors)
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return jsonify(success=True)
        else:
            flash('Ошибка входа. Проверьте имя пользователя и пароль. 🚫', 'danger')
            return jsonify(success=False, message='Ошибка входа. Проверьте имя пользователя и пароль.')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/add_location', methods=['POST'])
@login_required
def add_location():
    logging.debug('Получен запрос на добавление метки')
    form = LocationForm()
    if form.validate_on_submit():
        logging.debug('Форма прошла валидацию')
        try:
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])
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
            logging.debug('Метка успешно добавлена в базу данных')
            return jsonify(success=True)
        except Exception as e:
            logging.error('Ошибка при добавлении метки: %s', e)
            return jsonify(success=False, message=str(e))
    else:
        logging.debug('Ошибка валидации формы: %s', form.errors)
        return jsonify(success=False, message=form.errors)

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
