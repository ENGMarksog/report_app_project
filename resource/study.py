from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,  get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from database import db
from datetime import date
from schema import StudySchema, StudyUpdateSchema
from models.study_model import StudyModel

blp = Blueprint("Study_report", __name__, description = "a table holding study reports")

@blp.route("/study")
class StudyList(MethodView):

    @jwt_required()
    @blp.response(200, StudySchema(many=True))
    def get(self):
        return StudyModel.query.all() 
    
    @jwt_required(fresh=True)
    @blp.arguments(StudySchema)
    @blp.response(201, StudyUpdateSchema)
    def post(self, study_data):
        created = date.today()
        study = StudyModel(created = created, **study_data)
        try:
            db.session.add(study)
            db.session.commit()
        except IntegrityError:
            abort(400, message="this report already exist")
        except SQLAlchemyError:
            abort(500, message = "an error ocurred while saving study report to database")

        return study


@blp.route("/study/<string:created>")
class Study(MethodView):

    @jwt_required()
    @blp.response(200, StudySchema)
    def get(self, created):
        study = StudyModel.query.get_or_404(created)
        return study
    
    @jwt_required(fresh=True)
    @blp.arguments(StudyUpdateSchema)
    def put(self, study_data, created):
        study = StudyModel.query.get_or_404(created)
        if study:
            study.study_group = study_data["study_group"]
            study.messages_listened = study_data["messages_listened"]
            study.comment_study = study_data["comment_study"]
            study.created = date.today()
            
        else:
            study = StudyModel(**study_data)
        
        db.session.add(study)
        db.session.commit()

        return study
    
    @jwt_required()
    def delete(cls, created):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        study = StudyModel.query.get_or_404(created)
        db.session.delete(study)
        db.session.commit()
        return {"message": "study report deleted"}
