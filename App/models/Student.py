from App.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    totalHours = db.Column(db.Double, nullable=False)

    def __init__(self, name):
        self.name = name

    def request_confirmation(self, hours):
        self.totalHours += hours
        
    def view_leaderboard(self):
        students = Student.query.order_by(Student.totalHours.desc()).all()
        return students
    
    def view_accolades(self):
        return self.accolades