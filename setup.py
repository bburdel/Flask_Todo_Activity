"""
Scripts to run to set up database
"""

from datetime import datetime
from model import db, User, Task
from passlib.hash import pbkdf2_sha256

# Create the database tables
db.connect()
db.drop_tables([User, Task])
db.create_tables([User, Task])

# Create sample users
User(user_name="admin", user_password=pbkdf2_sha256.hash("password")).save()
User(user_name="bob", user_password=pbkdf2_sha256.hash("bobbob")).save()

# Create sample tasks
Task(task_name="Do the laundry.").save()
Task(task_name="Do the dishes.", task_performed=datetime.now(), performed_by='admin').save()
