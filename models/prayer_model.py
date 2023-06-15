from database import db


class PrayerModel(db.Model):
    __tablename__="prayer_info"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    worker_id = db.Column(db.String, db.ForeignKey("worker.worker_id"), nullable=False, unique=True) #foreign key
    created = db.Column(db.Date, nullable=True)
    prayer_group = db.Column(db.String(255), nullable=False)
    prayer_chain = db.Column(db.String, nullable=True)
    retreat = db.Column(db.String, nullable=True)
    vigil = db.Column(db.String, nullable=True)
    comment_prayer = db.Column(db.Text, nullable=True)

    worker = db.relationship("WorkerModel", back_populates="prayer_info")