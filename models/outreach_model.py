from database import db


class OutreachModel(db.Model):
    __tablename__ = "outreach_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    worker_id = db.Column(db.String, db.ForeignKey("worker.worker_id"), nullable=False, unique=True) # foreign key
    total_reached = db.Column(db.Integer, nullable=False)
    saved = db.Column(db.Integer, nullable=False)
    already_saved = db.Column(db.Integer, nullable=False)
    filled = db.Column(db.Integer, nullable=False)
    healed = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Date, nullable=False)
    comment_outreach = db.Column(db.String, nullable=True)

    worker = db.relationship("WorkerModel", back_populates="outreach_info")