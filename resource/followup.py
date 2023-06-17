from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from database import db
from datetime import date
from schema import FollowupSchema, FollowupUpdateSchema
from models.followup_model import FollowupModel

blp = Blueprint("Followup_report", __name__, description = "a table holding followup reports")

@blp.route("/followup")
class StudyList(MethodView):

    @jwt_required()
    @blp.response(200, FollowupSchema(many=True))
    def get(self):
        return FollowupModel.query.all() 
    
    @jwt_required(fresh=True)
    @blp.arguments(FollowupSchema)
    @blp.response(201, FollowupUpdateSchema)
    def post(self, followup_data):
        created = date.today()
        followup = FollowupModel(created = created, **followup_data)
        try:
            db.session.add(followup)
            db.session.commit()
        except IntegrityError:
            abort(400, message="this report already exist")
        except SQLAlchemyError:
            abort(500, message = "an error ocurred while saving followup report to database ")
        
        return followup


@blp.route("/followup/<string:created>")
class Study(MethodView):

    @jwt_required()
    @blp.response(200, FollowupSchema)
    def get(self, created):
        followup = FollowupModel.query.get_or_404(created)
        return followup
    
    @jwt_required(fresh=True)
    @blp.arguments(FollowupUpdateSchema)
    def put(self, followup_data, created):
        followup = FollowupModel.query.get_or_404(created)
        if followup:
            followup.duration = followup_data["duration"]
            followup.persons = followup_data["persons"]
            followup.comment_comment = followup_data["comment_followup"]
            followup.created = date.today()
            
        else:
            followup = FollowupModel(**followup_data)
        
        db.session.add(followup)
        db.session.commit()

        return followup
    
    @jwt_required(fresh=True)
    def delete(cls, created):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        followup = FollowupModel.query.get_or_404(created)
        db.session.delete(followup)
        db.session.commit()
        return {"message": "study report deleted"}
