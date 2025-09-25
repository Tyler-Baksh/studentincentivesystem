from App.database import db
from .Student import *

class ConfirmationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dateOfService = db.Column(db.String(120), nullable=False)
    activity = db.Column(db.String(120), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, dateOfService, activity, hours):
        num_hours  = int(hours)
        self.dateOfService = dateOfService
        self.activity = activity
        self.hours = num_hours
        self.status = 'Pending'

    def __repr__(self):
        return f'<Confirmation Request: {self.id}, Date: {self.dateOfService}, Activity: {self.activity}, Hour/s: {self.hours}>'