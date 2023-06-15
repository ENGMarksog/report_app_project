from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from database import db
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity

from datetime import date
import uuid
# add the database
from schema import WorkerSchema, WorkerUpdateSchema, WorkerAuth
from models.worker_model import WorkerModel
from blocklist import BLOCKLIST

blp = Blueprint("Worker_profile", __name__, description = "a table holding worker metadata")

@blp.route("/worker")
class WorkerList(MethodView):
    
    #reading all workers only for admins
    @jwt_required(fresh=True)
    @blp.response(200, WorkerSchema(many=True))
    def get(self):
        return WorkerModel.query.all() #only admins and specific role should have this access.
    

    #creating a worker 
    #to do: create and endpoint to create workers through signed users
    #@jwt_required()
    @blp.arguments(WorkerSchema)
    @blp.response(201, WorkerUpdateSchema)
    def post(self, worker_data):
        if WorkerModel.query.filter(WorkerModel.email == worker_data["email"]).first():
            abort(409, message="A worker with this email already exists.")

        worker_id =worker_data["last_name"][:4] + worker_data["first_name"][:4] + uuid.uuid4().hex[:6]
        created = date.today()
        password = pbkdf2_sha256.hash(worker_data["password"])
        worker = {**worker_data, "worker_id":worker_id, "created":created, "password":password}
        sc_worker = WorkerModel(**worker)
        
        try:
            db.session.add(sc_worker)
            db.session.commit()
        except IntegrityError:
            abort(400, message ="this worker already exist")
        except SQLAlchemyError as error:
            abort(500, message= f"a {type(error).__name__} error occured while saving worker to database: {error}")
        return sc_worker 
 
    
@blp.route("/worker/<string:worker_id>") #passing worker_id or email
class Worker(MethodView):
    #get specific person by rbac
    @jwt_required(fresh=True)
    @blp.response(200, WorkerSchema)
    def get(self, worker_id):
        worker = WorkerModel.query.get_or_404(worker_id) 
        return worker
    
    @jwt_required(fresh=True)
    @blp.arguments(WorkerUpdateSchema)
    def put(self, worker_data, worker_id):
        worker = WorkerModel.query.get_or_404(worker_id)
        if worker:
            worker.dob = worker_data["dob"]
            worker.location = worker_data["location"]
            worker.role = worker_data["role"]
            worker.disciples = worker_data["disciples"]
            worker.reports = worker_data["reports"]
            worker.pastor = worker_data["pastor"]
        else:
            worker = WorkerModel(worker_id = worker_id, **worker_data)
        
        db.session.add(worker)
        db.session.commit()

        return worker
        
    #should be only admin or specfic role to do this.
    @jwt_required(fresh=True)
    def delete(cls, worker_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        worker = WorkerModel.query.get_or_404(worker_id)
        db.session.delete(worker)
        db.session.commit()
        return {"message": "worker deleted"}, 200



@blp.route("/login")
class WorkerLogin(MethodView):
    @blp.arguments(WorkerAuth)
    def post(self, worker_data):
        worker = WorkerModel.query.filter(
            WorkerModel.email == worker_data["email"]
        ).first()

        if worker and pbkdf2_sha256.verify(worker_data["password"], worker.password):
            access_token = create_access_token(identity=worker.worker_id)
            refresh_token = create_refresh_token(worker.worker_id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
        abort(401, message="Invalid credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_worker = get_jwt_identity()
        new_token = create_refresh_token(identity=current_worker, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200

@blp.route("/logout")
class WorkerLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        print(jti)
        BLOCKLIST.add(jti)
        return {"message": "successfully logged out"}, 200

