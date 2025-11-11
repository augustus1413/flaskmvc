from App.database import db

class Accolade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    totalHours = db.Column(db.Double, db.ForeignKey('student.totalHours'), nullable=False)                                              
    awardDate = db.Column(db.Date, nullable=False)
    awardType = db.Column(db.String(200), nullable=False)
    milestoneHours = db.Column(db.Double, nullable=False)
    
    student = db.relationship('Student', backref=db.backref('accolades', lazy=True))

    def __init__(self, awardType, milestoneHours, awardDate):
        self.awardType = awardType
        self.milestoneHours = milestoneHours
        self.awardDate = db.func.current_date()