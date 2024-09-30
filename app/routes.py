from datetime import datetime

from sqlalchemy.future import select

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app as app
from flask_login import login_user, logout_user, current_user, login_required

from .database import get_async_engine, get_async_session
from .models import db, User, Location, Review, OwnerInfo
from .forms import RegistrationForm, LoginForm, LocationForm, OwnerInfoForm, ReviewForm
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    app.logger.info('Загрузка главной страницы')
    registration_form = RegistrationForm()
    login_form = LoginForm()
    location_form = LocationForm()
    owner_info_form = OwnerInfoForm()
    review_form = ReviewForm()
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    return render_template('index.html',
                           registration_form=registration_form,
                           login_form=login_form,
                           location_form=location_form,
                           owner_info_form=owner_info_form,
                           review_form=review_form,
                           google_maps_api_key=google_maps_api_key)

@bp.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        app.logger.info("Форма прошла валидацию")

        existing_user_by_username = User.query.filter_by(username=form.username.data).first()
        existing_user_by_phone = User.query.filter_by(phone_hash=form.phone.data).first()

        if existing_user_by_username:
            message = 'Пользователь с таким именем уже существует. 🚫'
            app.logger.info("Пользователь с таким именем уже существует.")
            return jsonify(success=False, message=message)

        if existing_user_by_phone:
            message = 'Пользователь с таким телефоном уже существует. 🚫'
            app.logger.info("Пользователь с таким телефоном уже существует.")
            return jsonify(success=False, message=message)

        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                second_name=form.second_name.data,
            )
            user.set_password(form.password.data)
            user.set_phone(form.phone.data)
            db.session.add(user)
            app.logger.info("Попытка коммита в базу данных")
            db.session.commit()
            message = 'Регистрация прошла успешно! 😊'
            app.logger.info("Пользователь успешно добавлен в базу данных")
            return jsonify(success=True, message=message)

        except Exception as e:
            app.logger.error(f"Ошибка при добавлении пользователя: {e}")
            db.session.rollback()
            return jsonify(success=False, message=f"Ошибка при добавлении пользователя: {e}")

    else:
        app.logger.warning("Форма не прошла валидацию")
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
            latitude = request.form.get('latitude', type=float)
            longitude = request.form.get('longitude', type=float)

            if latitude is None or longitude is None:
                raise ValueError("Latitude или Longitude отсутствует или неверного типа.")

            app.logger.debug('Координаты: %s, %s', latitude, longitude)
            new_location = Location(
                name=form.name.data,
                address=form.address.data,
                working_hours_start=form.working_hours_start.data,
                working_hours_end=form.working_hours_end.data,
                average_check=form.average_check.data,
                latitude=latitude,
                longitude=longitude,
                created_by=current_user.id
            )
            db.session.add(new_location)
            db.session.commit()
            message = 'Точка успешно добавлена! 😊'
            app.logger.info(message)
            return jsonify(success=True, message=message, location_id=new_location.id)
        except Exception as e:
            message = f'Произошла ошибка при добавлении метки: {e} 🚫'
            app.logger.error(message)
            return jsonify(success=False, message=message)
    else:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        message = f'Ошибки валидации формы: {", ".join(error_messages)} 🚫'
        app.logger.error(f'Ошибка валидации формы: {form.errors}')
        return jsonify(success=False, message=message)

@bp.route('/add_owner_info', methods=['POST'])
@login_required
def add_owner_info():
    form = OwnerInfoForm()  # Форма для добавления информации владельца
    if form.validate_on_submit():
        try:
            user_id = current_user.id
            location_id = request.form.get('location_id')
            website = request.form.get('website')
            owner_info = request.form.get('owner_info')

            app.logger.info(f'User ID: {user_id}, Location ID: {location_id}, Website: {website}, Owner Info: {owner_info}')

            if not location_id:
                raise ValueError("Location ID is missing.")

            owner_info_entry = OwnerInfo(user_id=user_id, location_id=int(location_id), website=website, owner_info=owner_info)
            db.session.add(owner_info_entry)
            db.session.commit()

            message = 'Информация о владельце успешно добавлена в базу данных! 😊'
            app.logger.info(message)
            return jsonify(success=True, message=message)
        except Exception as e:
            message = f'Произошла ошибка при добавлении информации: {e} 🚫'
            app.logger.error(message)
            return jsonify(success=False, message=message)
    else:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        message = f'Ошибки валидации формы: {", ".join(error_messages)} 🚫'
        app.logger.error(f'Ошибка валидации формы: {form.errors}')
        return jsonify(success=False, message=message)

@bp.route('/markers')
async def markers():
    engine = get_async_engine()
    async_session = get_async_session(engine)  # Получаем фабрику сессий

    async with async_session() as session:  # Создаем новую сессию
        result = await session.execute(select(Location))
        locations = result.scalars().all()

    markers = []
    for location in locations:
        markers.append({
            'id': location.id,
            'name': location.name,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'address': location.address,
            'working_hours': f"{location.working_hours_start} - {location.working_hours_end}",
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
            'user_name': review.user.username,
            'comment': review.comment,
            'rating': review.rating
        } for review in reviews
    ]
    return jsonify(reviews_list)

@bp.route('/add_review', methods=['POST'])
@login_required
def add_review():
    try:
        # Логируем полученные данные
        location_id_str = request.form.get('location_id', '').strip()
        app.logger.info(f"Received location_id: {location_id_str}")

        if not location_id_str:
            raise ValueError("Location ID is missing or invalid.")

        location_id = int(location_id_str)
        comment = request.form['comment'].strip()

        # Логируем полученный комментарий
        app.logger.info(f"Received comment: {comment}")

        # Проверка на существование отзыва
        existing_review = Review.query.filter_by(user_id=current_user.id, location_id=location_id).first()

        if existing_review:
            app.logger.info(f"Found existing review for location {location_id}")
            if existing_review.comment:
                app.logger.info(f"User already added a review for location {location_id}")
                return jsonify(success=False, message='Ваш отзыв уже добавлен.')
            else:
                existing_review.comment = comment
                existing_review.created_at = datetime.utcnow()
                db.session.commit()
                app.logger.info(f"Review updated for location {location_id}")
                return jsonify(success=True, message='Ваш отзыв успешно обновлен!')

        # Если отзыв не найден, создаем новый
        new_review = Review(user_id=current_user.id, location_id=location_id, comment=comment)
        db.session.add(new_review)
        db.session.commit()
        app.logger.info(f"New review added for location {location_id}")
        return jsonify(success=True, message='Ваш отзыв успешно добавлен!')

    except ValueError as ve:
        app.logger.error(f'Ошибка в данных формы: {ve}')
        return jsonify(success=False, message=f'Ошибка в данных формы: {ve}')

    except Exception as e:
        app.logger.error(f'Ошибка при добавлении отзыва: {e}')
        return jsonify(success=False, message=f'Ошибка при добавлении отзыва: {e}')

@bp.route('/rate_location', methods=['POST'])
@login_required
def rate_location():
    try:
        location_id = request.json['location_id']
        rating = int(request.json['rating'])

        # Логирование ID локации и начального действия
        app.logger.info(f'Проверка существования записи для локации {location_id} и пользователя {current_user.id}')

        # Проверка на существование оценки
        existing_review = Review.query.filter_by(user_id=current_user.id, location_id=location_id).first()

        if existing_review:
            app.logger.info(f'Найдена существующая запись для локации {location_id}: {existing_review}')
            if existing_review.rating is not None:
                app.logger.info(f'Пользователь {current_user.id} уже добавил оценку для локации {location_id}')
                return jsonify(success=False, message='Ваша оценка уже добавлена.')
            else:
                existing_review.rating = rating
                db.session.commit()
                app.logger.info(
                    f'Оценка для локации {location_id} успешно обновлена для пользователя {current_user.id}')
                return jsonify(success=True, message='Ваша оценка успешно обновлена!')
        else:
            # Создание новой записи, если не найдена существующая
            new_review = Review(user_id=current_user.id, location_id=location_id, rating=rating)
            db.session.add(new_review)
            db.session.commit()
            app.logger.info(f'Новая оценка для локации {location_id} добавлена пользователем {current_user.id}')
            return jsonify(success=True, message='Ваша оценка успешно добавлена!')

    except Exception as e:
        app.logger.error(f'Ошибка при сохранении оценки: {e}')
        return jsonify(success=False, message=f'Ошибка при сохранении оценки: {e}')

