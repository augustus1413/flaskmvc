import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Student, Staff, VolRecord, Accolade, Leaderboard
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    
    gina_user = User(id=1, username="gina", password="gina123")
    haily_user = User(id=2, username="haily", password="haily123")
    amarli_user = User(id=3, username="amarli", password="amarli123")
    
    gina= Student(id=1, name="Gina Inag", totalHours=120.5)
    haily= Student(id=2, name="Haily", totalHours=99.0)
    amarli= Student(id=3, name="Amarli", totalHours=75.0)
    
    david = Staff(id=1, name="David Beckles")
    emma = Staff(id=2, name="Emma Watson")
    john = Staff(id=3, name="John Smith")
    
    david_user = User(id=4, username="david", password="david123")
    emma_user = User(id=5, username="emma", password="emma123")         
    john_user = User(id=6, username="john", password="john123")
    
    gina_accolade = Accolade(id=1, title="Community Helper", description="Awarded for outstanding community service", studentId=1)
    haily_accolade = Accolade(id=2, title="Volunteer Star", description="Recognized for exceptional volunteer work", studentId=2)
    amarli_accolade = Accolade(id=3, title="Service Champion", description="Honored for dedication to service activities", studentId=3) 
    
    gina_volrecord = VolRecord(id=1, volType="Environmental Cleanup", totalHours=120.5, studentId=1)
    haily_volrecord = VolRecord(id=2, volType="Food Bank Assistance", totalHours=99.0, studentId=2)
    amarli_volrecord = VolRecord(id=3, volType="Animal Shelter Support", totalHours=75.0, studentId=3)
    
    Leaderboard(id=1, studentId=1, totalHours=120.5, rank=1)
    Leaderboard(id=2, studentId=2, totalHours=99.0, rank=2)
    Leaderboard(id=3, studentId=3, totalHours=75.0, rank=3)
    
    db.session.add_all([gina_user, haily_user, amarli_user, gina, haily, amarli, david, emma, john, david_user, emma_user, john_user, gina_accolade, haily_accolade, amarli_accolade, gina_volrecord, haily_volrecord, amarli_volrecord])
    db.session.commit()
    
    print('database intialized')

@app.cli.command("request-confirmation", help="Request confirmation for a student's hours")
def request_confirmation():
    student = Student.query.filter_by(name="Gina Inag").first()
    if student:
        student.request_confirmation(5.0)
        db.session.commit()
        print(f"Requested confirmation for {student.name}'s hours.")
    else:
        print("Student not found.")
        
@app.cli.command("view-leaderboard", help="View the leaderboard")
def view_leaderboard():
    students = Student.query.order_by(Student.totalHours.desc()).all()
    print("Leaderboard:")
    for student in students:
        print(f"{student.name}: {student.totalHours} hours")

@app.cli.command("view-accolades", help="View accolades for a student")
def view_accolades():
    student = Student.query.filter_by(name="Gina Inag").first()
    if student:
        accolades = student.view_accolades()
        print(f"Accolades for {student.name}:")
        for accolade in accolades:
            print(f"- {accolade.title}: {accolade.description}")
    else:
        print("Student not found.")
        
@app.cli.command("log-hours", help="Log hours for a student by a staff")
def log_hours():
    staff = Staff.query.filter_by(name="David Beckles").first()
    student = Student.query.filter_by(name="Gina Inag").first()
    if staff and student:
        staff.log_hours(student, 3.0)
        print(f"{staff.name} logged 3.0 hours for {student.name}.")
    else:
        print("Staff or Student not found.")
        
@app.cli.command("confirm-hours", help="Confirm hours for a student by a staff")
def confirm_hours():
    staff = Staff.query.filter_by(name="David Beckles").first()
    student = Student.query.filter_by(name="Gina Inag").first()
    if staff and student:
        staff.confirm_hours(student, 3.0)
        print(f"{staff.name} confirmed 3.0 hours for {student.name}.")
    else:
        print("Staff or Student not found.")
        
@app.cli.command("generate-rankings", help="Generate leaderboard rankings")
def generate_rankings():
    leaderboard = Leaderboard(1, 1, 0)  # Dummy initialization
    leaderboard.generate_rankings()
    print("Leaderboard rankings generated.")  
    
@app.cli.command("get-top-students", help="Get top students from the leaderboard")
def get_top_students():
    leaderboard = Leaderboard(1, 1, 0)  # Dummy initialization
    top_students = leaderboard.get_top_students(3)
    print("Top Students:")
    for entry in top_students:
        student = Student.query.get(entry.studentId)
        print(f"{student.name}: {entry.totalHours} hours (Rank: {entry.rank})")
        
@app.cli.command("update-hours", help="Update hours for a volunteer record")
def update_hours():
    vol_record = VolRecord.query.filter_by(id=1).first()  # Assuming we're updating the first vol record
    if vol_record:
        vol_record.update_hours(130.0)
        print(f"Updated hours for {vol_record.student.name} to {vol_record.totalHours}.")
    else:
        print("Volunteer record not found.")
        
@app.cli.command("check-milestones", help="Check and award milestones for a student's volunteer record")
def check_milestones():
    vol_record = VolRecord.query.filter_by(id=1).first()  # Assuming we're checking for the first vol record
    if vol_record:
        vol_record.check_milestones()
        print(f"Checked and awarded milestones for {vol_record.student.name}.")
    else:
        print("Volunteer record not found.")
        
@app.cli.command("list-users", help="List all users in the database")
def list_users():
    users = get_all_users()
    print("Users in the database:")
    for user in users:
        print(f"- {user.username}")
    
        
'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)