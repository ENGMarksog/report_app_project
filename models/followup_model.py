from database import db

class FollowupModel(db.Model):
    __tablename__ = "followup_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    worker_id = db.Column(db.String, db.ForeignKey("worker.worker_id"), nullable=False, unique=True) #relate from workers
    created = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    topic = db.Column(db.String(255), nullable=True)
    comment_followup = db.Column(db.Text, nullable=True)
    person = db.Column(db.Text, nullable=False)

    worker = db.relationship("WorkerModel", back_populates="followup_info")