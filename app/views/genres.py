from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.genre import GenreSchema
from app.helpers.decorators import auth_required, admin_required
from app.implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        # направляем новую форму
        req_json = request.json
        # создаем пользователя через DAO используя метод create
        genre = genre_service.create(req_json)
        # возвращаем заголовок - location
        return "", 201, {'location': f'/genres/{genre.id}'}


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        genre_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, bid):
        genre_service.delete(bid)
        return "", 204
