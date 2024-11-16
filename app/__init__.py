from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import redirect, url_for, request, flash

# Инициализация расширений
db = SQLAlchemy()  # Создание экземпляра SQLAlchemy для работы с базой данных
bcrypt = Bcrypt()  # Создание экземпляра Bcrypt для хеширования паролей
login_manager = LoginManager()  # Создание экземпляра LoginManager для управления сессиями пользователей

# Настройка login_manager
login_manager.login_view = 'main.login'  # Маршрут для перенаправления при неавторизованном доступе
login_manager.login_message = 'Please log in to access this page.'  # Flash-сообщение при неавторизованном доступе
login_manager.login_message_category = 'info'  # Категория flash-сообщения (для стилизации, например, с Bootstrap)

@login_manager.unauthorized_handler
def unauthorized():
    # Обработчик для случаев, когда пользователь пытается получить доступ без авторизации
    flash('You must log in to access this page.', 'danger')  # Показ сообщения об ошибке
    return redirect(url_for('main.login', next=request.endpoint))  # Перенаправление на страницу входа

def create_app():
    # Функция для создания и настройки экземпляра Flask-приложения
    app = Flask(__name__)  # Создание экземпляра Flask
    app.config['SECRET_KEY'] = 'your_secret_key'  # Установка секретного ключа для сессий
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Установка URI для подключения к базе данных

    # Инициализация расширений с привязкой к приложению
    db.init_app(app)  # Привязка экземпляра SQLAlchemy к приложению
    bcrypt.init_app(app)  # Привязка экземпляра Bcrypt к приложению
    login_manager.init_app(app)  # Привязка экземпляра LoginManager к приложению

    # Регистрация blueprint-ов
    from app.routes import main  # Импорт blueprint-а для маршрутов
    app.register_blueprint(main)  # Регистрация blueprint-а в приложении

    return app # Возврат готового экземпляра приложения
