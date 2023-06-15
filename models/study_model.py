from database import db


class StudyModel(db.Model):
    __tablename__="study_info"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    worker_id = db.Column(db.String, db.ForeignKey("worker.worker_id"), nullable=False, unique=True) #foreign key
    created = db.Column(db.Date, nullable=True)
    study_group = db.Column(db.String(255), nullable=False)
    messages_listened = db.Column(db.String(255), nullable=True)
    book_read = db.Column(db.String, nullable=True)
    comment_study = db.Column(db.Text, nullable=True)

    worker = db.relationship("WorkerModel", back_populates="study_info")