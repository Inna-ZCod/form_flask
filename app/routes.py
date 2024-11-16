from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm as ProfileForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, AnonymousUserMixin

# Этот файл определяет маршруты (routes) веб-приложения на Flask, связанные с пользователями.

# # Создаем объект Blueprint для определения маршрутов, связанных с основной частью приложения
main = Blueprint('main', __name__)

# Декоратор определяет маршрут для домашней страницы
@main.route('/')
def home():
    return render_template('home.html') #  # Возвращает шаблон home.html для отображения главной страницы


# Маршрут для регистрации нового пользователя, обрабатывает GET и POST запросы
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm() # Создаем экземпляр формы регистрации
    if form.validate_on_submit(): # Проверяем, если форма была валидирована и отправлена
        # Создаём нового пользователя с данными из формы
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data) # Хешируем пароль
        db.session.add(user) # Добавляем пользователя в сессию базы данных
        db.session.commit() # Сохраняем изменения в базе данных

        # Автоматически авторизуем нового пользователя после регистрации
        login_user(user)
        flash('Account created successfully! You are now logged in.', 'success') # Выводим сообщение об успешной регистрации

        # Перенаправляем пользователя на страницу профиля
        return redirect(url_for('main.profile'))

    # Если форма не валидирована или это GET-запрос, отображаем страницу регистрации с формой
    return render_template('register.html', form=form)


# Маршрут для входа в систему, обрабатывает GET и POST запросы
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # Создаем экземпляр формы логина
    if form.validate_on_submit():  # Проверяем, если форма была валидирована и отправлена
        user = User.query.filter_by(email=form.email.data).first()  # Ищем пользователя в базе данных по email
        if user and user.check_password(form.password.data): # Проверяем, если пользователь существует и пароль верный
            login_user(user) # Авторизуем пользователя
            flash('Login successful!', 'success') # Выводим сообщение об успешном входе

            # Проверяем параметр "next" в запросе, чтобы перенаправить пользователя на предыдущую страницу
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login failed. Check your email and password.', 'danger') # Выводим сообщение об ошибке входа
    return render_template('login.html', form=form) # Отображаем страницу входа с формой


# Маршрут для профиля пользователя, обрабатывает GET и POST запросы
@main.route('/profile', methods=['GET', 'POST'])
@login_required # Ограничение доступа только для авторизованных пользователей
def profile():
    if isinstance(current_user, AnonymousUserMixin): # Проверяем, если пользователь не авторизован
        flash('Please log in to access this page.', 'danger') # Выводим сообщение об ошибке доступа
        return redirect(url_for('main.login')) # Перенаправляем на страницу входа

    form = ProfileForm() # Создаем экземпляр формы обновления профиля

    if form.validate_on_submit(): # Проверяем, если форма была валидирована и отправлена
        # Обновляем данные текущего пользователя
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data: # Если пользователь ввел новый пароль, хешируем его
            current_user.set_password(form.password.data)

        db.session.commit() # Сохраняем изменения в базе данных
        flash('Profile updated!', 'success') # Выводим сообщение об успешном обновлении профиля
        return redirect(url_for('main.profile')) # Перенаправляем на страницу профиля

    # Заполняем форму текущими данными пользователя
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('profile.html', form=form) # Отображаем страницу профиля с формой


# Маршрут для выхода из системы
@main.route('/logout')
def logout():
    logout_user() # Выполняем выход пользователя
    flash('You have been logged out.', 'info')  # Выводим сообщение о выходе
    return redirect(url_for('main.login')) # Перенаправляем на страницу входа
