from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from database import db
from datetime import date
from schema import PrayerSchema, PrayerUpdateSchema
from models.prayer_model import PrayerModel

blp = Blueprint("Prayer_report", __name__, description = "a table holding prayer reports")

@blp.route("/prayer")
class PrayerList(MethodView):

    @jwt_required()
    @blp.response(200, PrayerSchema(many=True))
    def get(self):
        return PrayerModel.query.all() 
    
    @jwt_required()
    @blp.arguments(PrayerSchema)
    @blp.response(201, PrayerUpdateSchema)
    def post(self, prayer_data):
        created = date.today()
        prayer_rep = PrayerModel(created = created, **prayer_data)
        print(prayer_rep)
        try:
            db.session.add(prayer_rep)
            db.session.commit()
        except IntegrityError:
            abort(400, message="this report already exist")
        except SQLAlchemyError:
            abort(500, message = "an error ocurred while saving prayer report to database")

        return prayer_rep


@blp.route("/prayer/<string:created>")
class Prayer(MethodView):

    @jwt_required()
    @blp.response(200, PrayerSchema)
    def get(self, created):
        prayer = PrayerModel.query.get_or_404(created)
        return prayer
    
    @jwt_required()
    @blp.arguments(PrayerUpdateSchema)
    def put(self, prayer_data, created):
        prayer = PrayerModel.query.get_or_404(created)
        if prayer:
            prayer.prayer_chain = prayer_data["prayer_chain"]
            prayer.prayer_group = prayer_data["prayer_group"]
            prayer.comment_prayer = prayer_data["comment_prayer"]
            prayer.created = date.today()
            prayer.retreat = prayer_data["retreat"]
            prayer.vigil = prayer_data["vigil"]
        else:
            prayer = PrayerModel(**prayer_data)
        
        db.session.add(prayer)
        db.session.commit()

        return prayer
    
    @jwt_required()
    def delete(cls, created):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        prayer = PrayerModel.query.get_or_404(created)
        db.session.delete(prayer)
        db.session.commit()
        return {"message": "prayer report deleted"}
