from App.database import db
from .user import *
from .ConfirmationRequest import *
from .Achievement import *
from .StudentAchievement import *

class Student(User):
    __tablename__ = 'student'
    student_id = db.Column(db.String(120), unique=True)
    hours = db.Column(db.Integer)
    achievement_num = db.Column(db.Integer)
    confirmationRequests = db.relationship('ConfirmationRequest', backref='student', lazy=True, cascade="all, delete-orphan")
    achievements = db.relationship('Achievement', secondary='student_achievement', backref=db.backref('students', lazy=True))
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, student_id, hours, username, password):
        super().__init__(username, password)
        self.student_id = student_id
        self.achievement_num = 0
        self.hours = 0
        self.log_hours(hours)

    def __repr__(self):
        return f'<Student {self.student_id} : {self.username}>'
    
    def log_hours(self, hours):
        num_hours  = int(hours)
        self.hours = self.hours + num_hours
        a = Achievement.query.all()
        if self.hours >= 10 and self.achievement_num < 1:
            self.achievements.append(a[0])
            self.achievement_num = 1
        if self.hours >= 25 and self.achievement_num < 2:
            self.achievements.append(a[1])
            self.achievement_num = 2
        if self.hours >= 50 and self.achievement_num < 3:
            self.achievements.append(a[2])
            self.achievement_num = 3
