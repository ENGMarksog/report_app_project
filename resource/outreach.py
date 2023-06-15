from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import uuid

from database import db
from datetime import date, datetime
from schema import OutreachSchema, OutreachUpdateSchema
from models.outreach_model import OutreachModel

blp = Blueprint("Outreach_report", __name__, description = "a table holding outreach reports")

@blp.route("/outreach")
class OutreachList(MethodView):

    @jwt_required()
    @blp.response(200, OutreachSchema(many=True))
    def get(self):
        return OutreachModel.query.all() 
    
    @jwt_required()
    @blp.arguments(OutreachSchema)
    @blp.response(201, OutreachUpdateSchema)
    def post(self, outreach_data):
        created = date.today()
        outreach = OutreachModel(created = created,  **outreach_data)
        try:
            db.session.add(outreach)
            db.session.commit()
        except IntegrityError:
            abort(400, message="this report already exist")
        except SQLAlchemyError:
            abort(500, message = "an error ocurred while saving outreach report to database")
        
        return outreach


@blp.route("/outreach/<string:created>")
class Outreach(MethodView):

    @jwt_required()
    @blp.response(200, OutreachSchema)
    def get(self, created):
        outreach = OutreachModel.query.get_or_404(created)
        return outreach
    
    @jwt_required()
    @blp.arguments(OutreachUpdateSchema)
    def put(self, outreach_data, created):
        outreach = OutreachModel.query.get_or_404(created)
        if outreach:
            outreach.duration = outreach_data["duration"]
            outreach.saved = outreach_data["saved"]
            outreach.already_saved = outreach_data["already_saved"]
            outreach.healed = outreach_data["healed"]
            outreach.filled = outreach_data["filled"]
            outreach.comment_comment = outreach_data["comment_outreach"]
            outreach.created = date.today()
            
        else:
            outreach = OutreachModel(**outreach_data)
        
        db.session.add(outreach)
        db.session.commit()

        return outreach
    
    @jwt_required()
    def delete(cls, created):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        outreach = OutreachModel.query.get_or_404(created)
        db.session.delete(outreach)
        db.session.commit()
        return {"message": "study report deleted"}
