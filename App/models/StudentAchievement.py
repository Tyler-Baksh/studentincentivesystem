from App.database import db
from .Student import *
from .Achievement import *

class StudentAchievement(db.Model):
    __tablename__ ='student_achievement'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    