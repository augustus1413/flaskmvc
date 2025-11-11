from App.database import db

class VolRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    totalHours = db.Column(db.Double, db.ForeignKey('student.totalHours'), nullable=False)                                              
    volType = db.Column(db.String(200), nullable=False)
    isConfirmed = db.Column(db.Boolean, default=False, nullable=False)

    student = db.relationship('Student', backref=db.backref('volRecords', lazy=True))
    accolades = db.relationship('Accolade', backref='volRecord', lazy=True)
    
    def __init__(self, volType, totalHours):
        self.volType = volType
        self.totalHours = totalHours
        self.date = db.func.current_date()
        self.isConfirmed = False
        
    def update_hours(self, hours):
        self.totalHours = hours
        db.session.commit()
    
    def check_milestones(self):
        from .Accolade import Accolade
        milestones = [10, 25, 50]
        for milestone in milestones:
            if self.student.totalHours >= milestone:
                existing_accolade = Accolade.query.filter_by(studentId=self.studentId, milestoneHours=milestone).first()
                if not existing_accolade:
                    accolade = Accolade(awardType=f"{milestone} Hours Milestone", milestoneHours=milestone, awardDate=db.func.current_date())
                    accolade.studentId = self.studentId
                    db.session.add(accolade)
        db.session.commit()