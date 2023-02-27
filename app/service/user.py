# Сервис будет той управляющей структурой которая заберет на себя логику с проверками id,
# условиями на наличие полей и т.д.
import base64
import hashlib
import hmac

from app.dao.user import UserDAO
from app.helpers.constants import PWD_SALT, PWD_ITERATIONS


class UserService:
    # настраиваем зависимость с dao
    # сoздаем конструктор куда помещаем наш тип dao.
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, uid):
        return self.dao.get_by_username(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        # полученный набор данных будет перезаписывать поле password
        data['password'] = self.generate_password(data['password'])
        return self.dao.create(data)

    def delete(self, uid):
        self.dao.delete(uid)

    def update(self, data):
        # если передается пароль, то мы должны обновлять его через повторную генерацию хеша
        # здесь мы используем строку, которую возвращает фун-ция generate_password.
        data['password'] = self.generate_password(data['password'])
        # вызываем update dao
        self.dao.update(data)

    def generate_password(self, password):
        """
        Данная функция выполняет 2 операции: 1 получение бинарного
        представления, в виде некой последовательности чисел, которую
        мы назовем hash_digest.

        """
        # Используем библиотеку hashlib которую импортируем.
        # Здесь есть функция pbkdf2_hmac. Мы ее используем для того,
        # что бы на основании выбранного алгоритма и какой-то строки,
        # создать новую бинарную последовательность чисел.

        hash_digest = hashlib.pbkdf2_hmac(
            # алгоритм для генерации используется для получения секретной строки

            'sha256',  # фун-ция использует алгоритм sha256.

            # Передаем пароль, который получили в качестве аргумента, кодируя его
            # в бинарное представление. В кодировки utf-8.

            password.encode('utf-8'),  # фун-ия получает пароль в виде бинарных данныйх

            # константа некоторой дополнительной строки переведенной.

            PWD_SALT,  # фун-ия берет соль, это некоторые бинарные данные.

            # количество интераций, которые нужно выполнить.

            PWD_ITERATIONS  # фун-ция проводит 100_000 раз интерацию генерации пароля.
        )

        # воспользуемся библиотекой base64 у которой вызываем метод b64encode и передаем
        # в метод данные которые хотим закодировать.
        return base64.b64encode(hash_digest)  # возвращает строку.

    def compare_password(self, password_hash, other_password) -> bool:
        """
        Функция на проверку соответствия пароля из реквеста паролю БД
        """
        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
            )
        # вернет результат True или False если хеши равны или не равны
        return hmac.compare_digest(decoded_digest, hash_digest)
