# Приложение по поиску фильмов из базы данных

## Приложение на Flask 

***
Приложение позволяет находить фильмы авторизованным пользователям
по критериям поиска из базы данных, а так же удалять или изменять данные.
***

* Фильмы
* Жанры
* Режиссеры
* Пользователи

'''

def auth_required(func):

    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithm=[JWT_ALGORITHM])
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):

    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        # заводим переменную роль, ее мы и будем брать за основу проверки доступа.
        role = None

        try:
            # сохраняем результат декодирования в переменной юзер(логин, пароль, роль)
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            # извлекаем по ключу значение роль, и если оно не задано возьмем стандартное - user
            role = user.get('role', 'user')  # имея роль пользователя, можем ее проверить на совпадение с админом
        # если ошибка - выдаем 401 - не авторизован
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        # проверка на админа, если не админ, отдаем 403-доступ запрещен
        if role != 'admin':
            abort(403)
        # прокидываем в функцию все аргументы вызванные у декоратора.
        return func(*args, **kwargs)
    return wrapper

'''
