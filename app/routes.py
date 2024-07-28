from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from .models import db, User, Location, Review
from .forms import RegistrationForm, LoginForm, LocationForm
import logging
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    app.logger.info('Загрузка главной страницы')
    form = RegistrationForm()
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('index.html', form=form, google_maps_api_key=google_maps_api_key)

@bp.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user_by_username = User.query.filter_by(username=form.username.data).first()
        existing_user_by_phone = User.query.filter_by(phone_hash=form.phone.data).first()

        if existing_user_by_username:
            message = 'Пользователь с таким именем уже существует. 🚫'
            return jsonify(success=False, message=message)

        if existing_user_by_phone:
            message = 'Пользователь с таким телефоном уже существует. 🚫'
            return jsonify(success=False, message=message)

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
        message = 'Регистрация прошла успешно! 😊'
        return jsonify(success=True, message=message)
    else:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        message = f'Ошибка регистрации: {", ".join(error_messages)} 🚫'
        return jsonify(success=False, message=message)

@bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            message = 'Вход выполнен успешно! 😊'
            flash(message, 'success')
            app.logger.info(message)
            return jsonify(success=True, message=message)
        else:
            message = 'Ошибка входа. Проверьте имя пользователя и пароль. 🚫'
            flash(message, 'danger')
            app.logger.warning(message)
            return jsonify(success=False, message=message)
    else:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        message = f'Ошибки валидации формы: {", ".join(error_messages)} 🚫'
        flash(message, 'danger')
        app.logger.error(f'Ошибка валидации формы: {form.errors}')
        return jsonify(success=False, message=message)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    message = 'Вы успешно вышли из системы! 😊'
    flash(message, 'success')
    app.logger.info(message)
    return redirect(url_for('main.index'))

@bp.route('/add_location', methods=['POST'])
@login_required
def add_location():
    app.logger.debug('Получен запрос на добавление метки')
    form = LocationForm()
    if form.validate_on_submit():
        app.logger.debug('Форма прошла валидацию')
        try:
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])
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
            message = 'Метка успешно добавлена в базу данных! 😊'
            app.logger.info(message)
            return jsonify(success=True)
        except Exception as e:
            message = f'Произошла ошибка при добавлении метки: {e} 🚫'
            app.logger.error(message)
            return jsonify(success=False, message=message)
    else:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        message = f'Ошибки валидации формы: {", ".join(error_messages)} 🚫'
        app.logger.error(f'Ошибка валидации формы: {form.errors}')
        return jsonify(success=False, message=message)

@bp.route('/markers')
def markers():
    locations = Location.query.all()
    markers = []
    for location in locations:
        markers.append({
            'id': location.id,  # Убедитесь, что id включен
            'name': location.name,
            'description': location.description,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'address': location.address,
            'working_hours': location.working_hours,
            'average_check': location.average_check,
            'average_rating': location.average_rating,
            'rating_count': location.rating_count
        })
    app.logger.info('Список меток успешно загружен')
    return jsonify(markers)


@bp.route('/reviews/<int:location_id>')
def reviews(location_id):
    reviews = Review.query.filter_by(location_id=location_id).all()
    reviews_list = [
        {
            'user_name': review.user.username,  # Использование отношения для получения имени пользователя
            'comment': review.comment,
            'rating': review.rating
        } for review in reviews
    ]
    return jsonify(reviews_list)


@bp.route('/add_review', methods=['POST'])
@login_required
def add_review():
    try:
        location_id = request.form['location_id']
        rating = int(request.form['rating'])
        comment = request.form['comment']

        new_review = Review(
            user_id=current_user.id,
            location_id=location_id,
            rating=rating,
            comment=comment
        )
        db.session.add(new_review)
        db.session.commit()

        # Обновление среднего рейтинга и количества отзывов
        location = Location.query.get(location_id)
        reviews = Review.query.filter_by(location_id=location_id).all()
        total_ratings = sum([review.rating for review in reviews])
        location.rating_count = len(reviews)
        location.average_rating = total_ratings / location.rating_count if location.rating_count else 0
        db.session.commit()

        return jsonify(success=True, message='Отзыв успешно добавлен!')
    except Exception as e:
        app.logger.error(f'Ошибка при добавлении отзыва: {e}')
        return jsonify(success=False, message=f'Ошибка при добавлении отзыва: {e}')
