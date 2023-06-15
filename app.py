from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import models
import os
from dotenv import load_dotenv
from database import db
from resource.worker import blp as WorkerBlueprint
from resource.outreach import blp as OutreachBlueprint
from resource.followup import blp as FollowupBlueprint
from resource.prayer import blp as PrayerBlueprint
from resource.study import blp as StudyBlueprint
from blocklist import BLOCKLIST

def create_app(db_url=None):

    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "SCC REPORT API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL",  "sqlite:///report_db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "Authenticate"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1: #this the worker id to know who can do certain functions
            return {"is_admin":True}
        return {"is_admin":False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "the token has expired.", "error": "token_expired"}), 401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401
        )
    
    @jwt.unauthorized_loader
    def missing_toejn_callback(error):
        return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

    """
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {   
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
                }
            ),
            401,
        )
    """
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    #with app.app_context():
       # db.create_all()
    
    api.register_blueprint(WorkerBlueprint)
    api.register_blueprint(OutreachBlueprint)
    api.register_blueprint(FollowupBlueprint)
    api.register_blueprint(PrayerBlueprint)
    api.register_blueprint(StudyBlueprint)

    return app


"""
test = "I am just a test output"

@app.get("/test")
def get_test():
    return {"test": test}
"""
