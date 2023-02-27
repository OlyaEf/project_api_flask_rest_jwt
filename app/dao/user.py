# Класса DAO для взаимодействия модели и представления. Бизнес логика.
from app.dao.model.user import User


# нам понадобиться здесь реализовать CRUD (создание, чтение, обновление и удаление)
class UserDAO:
    """
    Для работы с БД DAO понадобится одна зависимость session,
    для того что бы внедрить зависимость и сипользовать db.sessiob:
     1.  Можно импортировать from app.database import db
     2. Либо явно передать в DAO нужную сессию, если в последующем
     мы захотим первести нашу модель с sqlite на что-то другое и тогда
     сессия понадобиться втора
    """
    # создаем конструктор, который принимает объект session и сохранять его в себя.
    # Зависимость на sessions у нашего dao
    def __init__(self, session):
        self.session = session

    # Create
    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    # Create
    def get_all(self):
        return self.session.query(User).all()

    # Create (создание новой записи).
    # Создание и сохранение это логика нашего DAO
    def create(self, data):
        entity = User(**data)
        self.session.add(entity)
        self.session.commit()
        return entity

    # Update
    def update(self, data):
        # получаем id автора
        uid = data.get('id')
        # получаем автора
        user = self.get_one(uid)
        # обновляем данные
        if 'username' in data:
            user.username = data.get('username')
        if 'password' in data:
            user.password = data.get('password')
        if 'role' in data:
            user.role = data.get('role')
        # добавить и записать
        self.session.add(user)
        self.session.commit()
        return user

    # Delete
    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()
