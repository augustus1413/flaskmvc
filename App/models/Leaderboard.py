from App.database import db
from .Student import Student

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    totalHours = db.Column(db.Double, db.ForeignKey('student.totalHours'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    
    student = db.relationship('Student', backref=db.backref('leaderboard', lazy=True))

    def __init__(self, studentId, rank, totalHours):
        self.studentId = studentId
        self.rank = rank
        
    def generate_rankings(self):
        students = Student.query.order_by(Student.totalHours.desc()).all()
        for index, student in enumerate(students):
            leaderboard_entry = Leaderboard.query.filter_by(studentId=student.id).first()
            if leaderboard_entry:
                leaderboard_entry.rank = index + 1
                leaderboard_entry.totalHours = student.totalHours
            else:
                new_entry = Leaderboard(studentId=student.id, rank=index + 1, totalHours=student.totalHours)
                db.session.add(new_entry)
        db.session.commit()
        
    def get_top_students(self, limit=10):
        return Leaderboard.query.order_by(Leaderboard.rank).limit(limit).all()