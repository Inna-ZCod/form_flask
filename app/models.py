from app import login_manager # импортируется объект `login_manager`, который управляет сессиями пользователей
from app import db, bcrypt # импортируются объекты `db` (для работы с базой данных) и `bcrypt` (для хеширования паролей).
from flask_login import UserMixin # импортируется `UserMixin`, который добавляет необходимые методы для работы с Flask-Login.

# Этот файл содержит основную логику модели пользователя, включая управление паролями и интеграцию с системой аутентификации Flask.

# Модель, описывающая таблицу пользователей в базе данных. Она наследуется от `db.Model` (для поддержки работы с SQLAlchemy)
# и `UserMixin` (для интеграции с Flask-Login).
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # первичный ключ, который автоматически увеличивается.
    username = db.Column(db.String(20), unique=True, nullable=False) # строка длиной до 20 символов, должна быть уникальной и не может быть пустой.
    email = db.Column(db.String(120), unique=True, nullable=False) # строка длиной до 120 символов, также должна быть уникальной и не может быть пустой.
    password_hash = db.Column(db.String(128), nullable=False) # строка для хранения хеша пароля, не может быть пустой.

# принимает пароль, хеширует его с помощью `bcrypt` и сохраняет в `password_hash`.
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# проверяет, соответствует ли переданный пароль сохраненному хешу, возвращает `True`, если пароли совпадают.
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader # декоратор делает функцию загрузчиком пользователя для Flask-Login.
def load_user(user_id): # Принимает `user_id` и возвращает объект `User`, загруженный из базы данных по этому ID. Это необходимо для восстановления данных пользователя из сессии.
    return User.query.get(int(user_id))
