from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    scenario_type = db.Column(db.String(20), nullable=False, default="text")  # email, link, image, text
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(300), nullable=True)
    is_phishing = db.Column(db.Boolean, nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    answers = db.relationship("TestAnswer", backref="question", lazy=True)


class TestSession(db.Model):
    __tablename__ = "test_sessions"

    id = db.Column(db.String(36), primary_key=True)  # UUID
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(200), nullable=False)
    question_ids = db.Column(db.Text, nullable=False)  # JSON array
    current_index = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    answers = db.relationship("TestAnswer", backref="session", lazy=True)

    @property
    def total_questions(self):
        import json
        return len(json.loads(self.question_ids))

    @property
    def is_complete(self):
        return self.completed_at is not None

    @property
    def duration_minutes(self):
        if self.completed_at:
            delta = self.completed_at - self.started_at
            return round(delta.total_seconds() / 60, 1)
        return None


class TestAnswer(db.Model):
    __tablename__ = "test_answers"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey("test_sessions.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    user_answer = db.Column(db.Boolean, nullable=False)  # True=phishing, False=legitimate
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
