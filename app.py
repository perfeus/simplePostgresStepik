# для выполнения миграций установить Flask-Migrate
# для доступа к PostgreSQL в SQLAlchemy установить psycopg2-binary

import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Количество отображаемых визитов
MAX_VISITS = 5

app = Flask(__name__)
# Настраиваем приложение
app.config["DEBUG"] = True
# - URL доступа к БД берем из переменной окружения DATABASE_URL
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Создаем подключение к БД
db = SQLAlchemy(app)
# Создаем объект поддержки миграций
migrate = Migrate(app, db)

# Модель для хранения визитов нашей страницы
class Visit(db.Model):
    # Таблица
    __tablename__ = 'visits'

    id = db.Column(db.Integer, primary_key=True)
    # Автозаполняемое поле даты и времени
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())

# Наша единственная страница
@app.route('/')
def home():
    # Сохраняем текущее посещение
    visit = Visit()
    db.session.add(visit)
    db.session.commit()
    # Получаем последние MAX_VISITS посещения
    visits = Visit.query \
        .order_by(Visit.created_at.desc()) \
        .limit(MAX_VISITS) \
        .all()
	# Отображаем список посещений
    return render_template("home.html", visits=visits)
