from database import db

class WorkerModel(db.Model):
    __tablename__="worker"

    worker_id = db.Column(db.String(10), primary_key=True, unique=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(50), nullable=False)
    church_role = db.Column(db.String)
    disciples = db.Column(db.String(1000), nullable=True)
    reports = db.Column(db.String(50), nullable=False)
    pastor = db.Column(db.String(50), nullable=False)
    created = db.Column(db.Date)

    followup_info = db.relationship("FollowupModel", back_populates="worker", lazy="dynamic")
    outreach_info = db.relationship("OutreachModel", back_populates="worker", lazy="dynamic")
    prayer_info = db.relationship("PrayerModel", back_populates="worker", lazy="dynamic")
    study_info = db.relationship("StudyModel", back_populates="worker", lazy="dynamic")

