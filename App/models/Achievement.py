from App.database import db

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'<Achievement {self.id} - {self.text}>'