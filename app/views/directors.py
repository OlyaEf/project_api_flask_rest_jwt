from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.director import DirectorSchema
from app.helpers.decorators import auth_required, admin_required
from app.implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        # направляем новую форму
        req_json = request.json
        # создаем пользователя через DAO используя метод create
        director = director_service.create(req_json)
        # возвращаем заголовок - location
        return "", 201, {'location': f'/genres/{director.id}'}


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        director_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, bid):
        director_service.delete(bid)
        return "", 204