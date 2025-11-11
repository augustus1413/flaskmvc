from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
   
    student = db.relationship('Student', backref=db.backref('staff', lazy=True))
   
    def __init__(self, name):
        self.name = name
    
    def log_hours(self, student, hours):
        student.reqest_confirmation(hours)
        db.session.commit()
        
    def confirm_hours(self, student, hours):
        student.totalHours += hours
        db.session.commit()
        
    
    
    