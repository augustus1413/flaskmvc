![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Student Incentive System

A command-line application to manage student volunteering hours, accolades, and leaderboards.

---

## Features
- Staff can log and confirm student volunteering hours.
- Students can view their total hours, accolades, and leaderboard rankings.
- Milestones trigger accolades (e.g., 10, 25, 50 hours).
- Leaderboard ranks students based on total confirmed hours.

---

## CLI Commands

### `init`
**Description:**  
Creates and initializes the database with sample users, students, staff, volunteer records, accolades, and leaderboard entries.

**Usage:**  
```bash
flask init

### `request-confirmation`
**Description:**  
Student requests confirmation for a specified number of volunteer hours.

**Usage:**  
```bash
flask request-confirmation

### `view-leaderboard`
**Description:**  
Displays the leaderboard showing students ranked by their total volunteer hours.

**Usage:**  
```bash
flask view-leaderboard

### `view-accolades`
**Description:**  
Displays accolades earned by a specific student.

**Usage:**  
```bash
flask view-accolades

### `log-hours`
**Description:**
Staff logs volunteer hours for a student.

**Usage:**  
```bash
flask log-hours

### `confirm-hours`
**Description:**
Staff confirms volunteer hours for a student.

**Usage:**  
```bash
flask confirm-hours

### `generate-rankings`
**Description:**
Generates and updates the leaderboard rankings based on students' total volunteer hours.

**Usage:**  
```bash
flask generate-rankings

### `get-top-students`
**Description:**
Retrieves and displays the top students from the leaderboard.

**Usage:**  
```bash
flask get-top-students

### `update-hours`
**Description:**
Updates the volunteer hours for a specific volunteer record.

**Usage:**  
```bash
flask update-hours

### `check-milestones`
**Description:**
Checks and awards milestone accolades for a student's volunteer record based on hours completed.

**Usage:**  
```bash
flask check-milestones

### `list-users`
**Description:**
Lists all users currently in the database.

**Usage:**  
```bash
flask list-users

## Initialization Data Summary

The `init` command populates the database with the following sample data:

- **Users:**
  - Gina (Student) — username: `gina`, password: `gina123`
  - Haily (Student) — username: `haily`, password: `haily123`
  - Amarli (Student) — username: `amarli`, password: `amarli123`
  - David (Staff) — username: `david`, password: `david123`
  - Emma (Staff) — username: `emma`, password: `emma123`
  - John (Staff) — username: `john`, password: `john123`

- **Students:**
  - Gina Inag — total volunteer hours: 120.5
  - Haily — total volunteer hours: 99.0
  - Amarli — total volunteer hours: 75.0

- **Staff:**
  - David Beckles
  - Emma Watson
  - John Smith

- **Accolades:**
  - Community Helper (Gina Inag) — Awarded for outstanding community service
  - Volunteer Star (Haily) — Recognized for exceptional volunteer work
  - Service Champion (Amarli) — Honored for dedication to service activities

- **Volunteer Records:**
  - Environmental Cleanup (Gina Inag) — 120.5 hours
  - Food Bank Assistance (Haily) — 99.0 hours
  - Animal Shelter Support (Amarli) — 75.0 hours

- **Leaderboard:**
  - Rank 1: Gina Inag — 120.5 hours
  - Rank 2: Haily — 99.0 hours
  - Rank 3: Amarli — 75.0 hours

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
```


# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
