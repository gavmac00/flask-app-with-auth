from . import db # from website import db
from flask_login import UserMixin # UserMixin is a class that gives us access to certain attributes
from sqlalchemy.sql import func # func is a function that allows us to use SQL functions
from datetime import datetime

class User(db.Model, UserMixin): # UserMixin gives us access to certain attributes
    """Stores the user data."""
    id = db.Column(db.Integer, primary_key=True) # primary key is a unique identifier for each user
    email = db.Column(db.String(150), unique=True) # unique=True means that no two users can have the same email
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # relationship is a data type that allows us to access the notes of a user, note that it is capitalized because it is a class

class Note(db.Model):
    """Stores the note data."""
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # DateTime is a data type that stores the date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # ForeignKey is a data type that stores the id of another table, in this case the user table, note that it is not capitalized because it is a column