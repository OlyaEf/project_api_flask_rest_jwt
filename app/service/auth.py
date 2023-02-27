import calendar
import datetime

from flask import abort

import jwt

from app.helpers.constants import JWT_SECRET, JWT_ALGORITHM
from app.service.user import UserService


class AuthService:
    # AuthService в качестве зависимостей имеет UserService, т.е. мы можем обращаться к нему для получения пользователей
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    # получив юзернейм и пароль мы можем найти нужного нам пользователя
    def generate_tokens(self, username, password, is_refresh=False):
        # полученного пользователя сохраняем во временной переменной user
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)
        # если пользователь найден, вызываем юзер_сервер метод compare_password
        # передаем пароль(хэш) у найденного пользователя, и передаем сам пароль (чистый

        # проверяем соответствие паролей, если это создание токена, а не перегенерация на основании рефреш_токена.
        if not is_refresh:  # если is_refresh=False проверяем соответствие паролей, если True - не проверяем.
            if not self.user_service.compare_password(user.password, password):
                abort(400)

        # если пароль хэш и пароль чистый равны, то формируем набор данных:
        data = {
            'user': user.username,
            'role': user.role
        }

        # 30 минут для доступа с помощью токена
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # 130 дней для обновления токена
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Мы отдаем как access_token, так и refresh_token.
        # Как только пройдет 30 мин. с момента регенерации токена, наш клиент
        # сможет использовать рефрешь токен.
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        # Используя подход с декодированием токена. Получаем информацию о пользователе.
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithm=[JWT_ALGORITHM])
        # Из data мы можем извлечь имя пользователя.
        # И, так как нам прислали рефрешь токент то мы доверяем это клиенту и не требуем пароля.
        username = data.get("username")

        user = self.user_service.get_by_username(username=username)

        if user is None:
            raise Exception("")

        return self.generate_tokens(username, user.password, is_refresh=True)
