import peewee as pw
import os

from playhouse.db_url import connect

# connect to the database URL
db = connect(os.environ.get('DATABSE_URL', 'sqlite:///my_database.db'))


# create a base model for inheritance
class BaseModel(pw.Model):
    """
    A base model that Model classes inherit from
    """

    class Meta:
        database = db


class User(BaseModel):
    """
    This class defines the User, which maintains details of a user of ato do list app
    """
    user_name = pw.CharField(max_length=35, unique=True)
    user_password = pw.CharField(max_length=255)


class Task(BaseModel):
    """
    This class defines a Task, which maintains the details of a to do list task.
    """
    task_name = pw.CharField(max_length=255)
    task_performed = pw.DateTimeField(null=True)
    performed_by = pw.ForeignKeyField(model=User, null=True)

