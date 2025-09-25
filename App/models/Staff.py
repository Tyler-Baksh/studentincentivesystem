from App.database import db
from .user import *

class Staff(User):
    __tablename__ = 'staff'
    staff_id = db.Column(db.String(120), unique=True)
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, staff_id, username, password):
        super().__init__(username, password)
        self.staff_id = staff_id

    def __repr__(self):
        return f'<Staff {self.staff_id} : {self.username}>'