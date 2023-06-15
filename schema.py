from marshmallow import Schema, fields, ValidationError

class PlainWorkerSchema(Schema):
    worker_id = fields.Str(dump_only=True)
    created = fields.Str(dump_only=True)
    email = fields.Email()
    password = fields.Str(required=True, load_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    dob = fields.Str()
    location = fields.Str(required=True)
    role = fields.Str(required=True)
    disciples = fields.Str()
    reports = fields.Str(required=True)
    pastor = fields.Str(required=True)
    church_role = fields.Str()


class WorkerUpdateSchema(Schema):
    worker_id = fields.Str(dump_only=True)
    created = fields.Str(dump_only=True)
    email = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    dob = fields.Str()
    location = fields.Str()
    role = fields.Str()
    disciples = fields.Str()
    reports = fields.Str()
    pastor = fields.Str()

 #bug fix for prayer schema   
class PlainPrayerSchema(Schema):
    id = fields.Str(dump_only=True)
    created = fields.Str(dump_only=True)
    prayer_group = fields.Str(required=True)
    prayer_chain = fields.Str()
    comment_prayer = fields.Str()
    retreat = fields.Str()
    vigil = fields.Str()

class PrayerSchema(PlainPrayerSchema):
    worker_id = fields.Str()
    worker = fields.Nested(PlainPrayerSchema(), dump_only=True)

class PrayerUpdateSchema(Schema):
    created = fields.Date(dump_only=True)
    worker_id = fields.Str(dump_only=True)
    prayer_group = fields.Str(required=True)
    prayer_chain = fields.Str()
    comment_prayer = fields.Str()
    retreat = fields.Str()
    vigil = fields.Str()

#for Study Schema
class PlainStudySchema(Schema):
    id = fields.Str(dump_only=True)
    created = fields.Str(dump_only=True)
    study_group = fields.Str(required=True)
    messages_listened = fields.Str()
    comment_study = fields.Str()
    book_read = fields.Str()

class StudySchema(PlainStudySchema):
    worker_id = fields.Str()
    worker = fields.Nested(PlainStudySchema(), dump_only=True)

class StudyUpdateSchema(Schema):
    created = fields.Date(dump_only=True)
    worker_id = fields.Str(dump_only=True)
    study_group = fields.Str()
    message_listened = fields.Str()
    book_read = fields.Str()
    comment_study = fields.Str()

#for outreach Schema
class PlainOutreachSchema(Schema):
    id = fields.Int(dump_only=True)
    total_reached = fields.Int(required=True)
    saved = fields.Int(required=True)
    already_saved = fields.Int(required=True)
    filled = fields.Int(required=True)
    healed = fields.Int(required=True)
    duration = fields.Int(required=True)
    comment_outreach = fields.Str()
    created = fields.Date()

class OutreachSchema(PlainOutreachSchema):
    worker_id = fields.Str()
    worker = fields.Nested(PlainOutreachSchema(), dump_only=True)

class OutreachUpdateSchema(Schema):
    created = fields.Date(dump_only=True)
    worker_id = fields.Str(dump_only=True)
    total_reached = fields.Int()
    saved = fields.Str()
    already_saved = fields.Int()
    filled = fields.Int()
    healed = fields.Int()
    duration = fields.Int()
    comment_outreach = fields.Str()

# For followup
class PlainFollowupSchema(Schema):
    id = fields.Str(dump_only=True)
    created = fields.Date()
    duration = fields.Int(required=True)
    comment_followup = fields.Str()
    person = fields.Str() 
    topic = fields.Str()

class FollowupSchema(PlainFollowupSchema):
    worker_id = fields.Str()
    worker = fields.Nested(PlainFollowupSchema(), dump_only=True)

class FollowupUpdateSchema(Schema):
    created = fields.Date(dump_only=True)
    worker_id = fields.Str(dump_only=True)
    duration = fields.Int()
    comment_followup = fields.Str()
    person = fields.Str()
    topic = fields.Str()

class WorkerSchema(PlainWorkerSchema):
    prayer = fields.List(fields.Nested(PlainPrayerSchema()), dump_only=True)
    study = fields.List(fields.Nested(PlainStudySchema()), dump_only=True)
    outreach = fields.List(fields.Nested(OutreachSchema(), dump_only=True))
    followup = fields.List(fields.Nested(FollowupSchema(), dump_only=True))

class WorkerAuth(Schema):
    worker_id = fields.Str(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)