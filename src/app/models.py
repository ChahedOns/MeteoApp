from flask_login import UserMixin
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
import re
from flask_login import current_user
from wtforms import ValidationError
import datetime
from app import db

# Needed functions

def safe_string():
    """Validates that the field matches some safe requirements
    Used to make sure our user's username is safe and readable
    Requirements:
    - contains only letters, numbers, dashes and underscores
    """

    def validation(form, field):
        string = field.data.lower()
        pattern = re.compile(r"^[a-z0-9_-]+$")
        match = pattern.match(string)
        if not match:
            message = "Must contain only letters, numbers, dashes and underscores."
            raise ValidationError(message)

    return validation


def unique_or_current_user_field(message=None):
    """Validates that a field is either equal to user's current field
    or doesn't exist in the database
    Used for username and email fields
    """

    def validation(form, field):
        kwargs = {field.name: field.data}
        if (
            hasattr(current_user, field.name)
            and getattr(current_user, field.name) == field.data
        ):
            return
        if User.objects(**kwargs).first():
            raise ValidationError(message)

    return validation

#Documents definitions

class User(db.Document):
    username = db.StringField(required=True, unique=True, max_length=40, index=True)
    name = db.StringField(required=False, max_length=80, index=True)
    email = db.EmailField(
        unique=True, required=False, sparse=True, max_length=80, index=True
    )
    password = db.StringField(required=False, index=True)
    birth_date = db.DateTimeField(required=True)
    location=db.StringField(required=True)
    
    def to_json(self):
        return {
            "ID": self.ref,
            "Mail":self.mail,
            "Name":self.name,
            "Birthday":self.birth_date,
            "Location":self.location
        }
    def check_password(self, password):
        """Checks that the pw provided hashes to the stored pw hash value"""
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
            """Define what is printed for the user object"""
            return f"Username: {self.username} id: {self.id}"
    
class Place(db.Document):
    name=db.StringField(required=True)
    lat=db.FloatField()
    lon=db.StringField()

    def to_json(self):
        return{
            "Name": self.name,
            "Lat":self.lat,
            "Lon":self.lon
        }

class Weather(db.Document):
    data=db.DictField()
    date=db.DateField(default=datetime.datetime.now)
    city=db.StringField()
    def to_json(self):
        return{
            "Data": self.data,
            "Date":self.date,
            "City":self.city
        }
