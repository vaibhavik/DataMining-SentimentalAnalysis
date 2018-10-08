from django.db import models
from mongoengine import *

# Create your models here.

class Employee(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
class MovieOmdb(Document):
	title = StringField()
	year = StringField()
	genre = StringField()
	actors = StringField()
	poster = StringField()
	imdbrating = StringField()
	twitterrating = StringField()