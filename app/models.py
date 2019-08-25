from app import db


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.Integer, db.ForeignKey("web_sources.id"), nullable=False)
    event_name = db.Column(db.String(64), nullable=False)
    event_start = db.Column(db.Date, nullable=False)
    event_end = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
    )

    def __repr__(self):
        return "Event {}".format(self.event_name)


class WebSource(db.Model):
    __tablename__ = "web_sources"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    events = db.relationship("Event", backref="source")

    def __repr__(self):
        return "WebSource {}".format(self.source_name)
