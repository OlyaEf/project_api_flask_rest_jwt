# Описываем модель Author

# DAO - Data Access Object (Объект доступа к данным) - прослойка между БД и системой (логика работы с БД)
# Вынесенные модели умеют работать только со своим описанием

from marshmallow import Schema, fields

from app.setup_db import db


class User(db.Model):
    # указываем какая у нас таблица
    __tablename__ = 'user'
    # указываем колонки
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))


# Готовим схему для сериализации и десериализации через маршмалоу
class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()