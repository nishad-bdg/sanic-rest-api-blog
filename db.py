import datetime
from peewee import *

db = MySQLDatabase('tweets', user='root',password = '', charset='utf8mb4')

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField( unique = True)
    password = CharField()
    join_date = DateTimeField(default = datetime.datetime.now)



class Tweet(BaseModel):
    user = ForeignKeyField(User, backref = 'tweets')
    message = TextField()
    created = DateTimeField( default = datetime.datetime.now)
    is_published = BooleanField(default = True)

def create_table():
    db.create_tables([User,Tweet])









