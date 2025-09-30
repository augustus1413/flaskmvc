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
    
    gina = Student(id=10, name="Gina Inag", totalHours=120.5)
    haily = Student(id=20, name="Haily Yliah", totalHours=99.0)
    amarli = Student(id=30, name="Amarli Ilram", totalHours=75.0)
    
    david = Staff(id=11, name="David Beckles")
    emma = Staff(id=22, name="Emma Watson")
    john = Staff(id=33, name="John Smith")
    
    david_user = User(id=4, username="david", password="david123")
    emma_user = User(id=5, username="emma", password="emma123")         
    john_user = User(id=6, username="john", password="john123")
    
    gina_accolade = Accolade(id=14, title="Community Helper", description="Awarded for outstanding community service", studentId=1)
    haily_accolade = Accolade(id=24, title="Volunteer Star", description="Recognized for exceptional volunteer work", studentId=2)
    amarli_accolade = Accolade(id=34, title="Service Champion", description="Honored for dedication to service activities", studentId=3) 
    
    gina_volrecord = VolRecord(id=15, volType="Environmental Cleanup", totalHours=120.5, studentId=1)
    haily_volrecord = VolRecord(id=25, volType="Food Bank Assistance", totalHours=99.0, studentId=2)
    amarli_volrecord = VolRecord(id=35, volType="Animal Shelter Support", totalHours=75.0, studentId=3)
    
    Leaderboard(id=16, studentId=17, totalHours=120.5, rank=1)
    Leaderboard(id=26, studentId=27, totalHours=99.0, rank=2)
    Leaderboard(id=36, studentId=37, totalHours=75.0, rank=3)

    db.session.add_all([gina_user, haily_user, amarli_user, gina, haily, amarli, david, emma, john, david_user, emma_user, john_user, gina_accolade, haily_accolade, amarli_accolade, gina_volrecord, haily_volrecord, amarli_volrecord])
    db.session.commit()
    
    print('database intialized')

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