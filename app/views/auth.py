from flask import request
from flask_restx import Namespace, Resource

from app.implemented import auth_services

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthsView(Resource):
    # при получении запроса
    def post(self):
        """
        Метод получает логин и пароль из Body запроса в виде JSON,
        далее проверяет соотвествие с данными в БД (есть ли такой пользователь, такой ли у него пароль)
        и если всё оk — генерит пару access_token и refresh_token и отдает их в виде JSON.
        """
        # берем информацию из нашего запроса, из request.json
        # и, складываем ее в дата
        data = request.json

        # получаем два значения пользователь и пароль
        username = data.get('username', None)
        password = data.get('password', None)

        # проверяем что бы они были заполнены
        if None is [username, password]:
            return '', 400

        # если все ок - вызываем аут_сервис и метод генерация токена.
        tokens = auth_services.generate_tokens(username, password)

        return tokens, 201

    def put(self):
        """
        Метод получает refresh_token из Body запроса в виде JSON, далее проверяет refresh_token
        и если он не истек и валиден — генерит пару access_token и refresh_token и отдает их в виде JSON.
        """
        data = request.json
        token = data.get('refresh_token')

        tokens = auth_services.approve_refresh_token(token)

        return tokens, 201
