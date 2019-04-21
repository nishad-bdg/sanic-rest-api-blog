from sanic import Sanic
from sanic.response import html
from sanic.views import HTTPMethodView
from sanic.response import text
from sanic import response
from sanic_jwt import exceptions,initialize
from sanic_jwt.decorators import protected
import json
from db import *
import hashlib, binascii
import os

async def authenticate(request, *args, **kwargs):
    username = request.json.get("username",None)
    password = request.json.get("password",None)
    hash_password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    
    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password")
    try:
        user = User.get(username = username, password = hash_password)
    except:
        raise exceptions.AuthenticationFailed("Invalid username or password")
    return {"user_id": user.id}


app = Sanic(__name__)
app.static('/public','./public')
initialize(app, authenticate = authenticate)

class UserList(HTTPMethodView):
    decorators = [protected()]
    async def get(self, request):
        users = []
        for user in User.select():
            users.append({"username": user.username, "password": user.password, "join_date": user.join_date})
        return response.json(users)
    
    async def post(self, request):
        message = {}
        post = request.json
        username = post['username']
        password = post['password']

        if username == "":
            message['error'] = "username is required"
        elif len(username) < 6:
            message['error'] = "username must be atleast 6 chars"
        elif password == "":
            message['error'] = "password is required"
        elif len(password) < 6:
            message['error'] = "password must be atleast 6 chars"
            
        else:
            hash_password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
            insert = User.create(username = username, password = hash_password)
            message['success'] = "User created successfully"
            return response.json({'message': message, 'status': 201})

        return response.json({'message': message})




 

class TweetList(HTTPMethodView):

    async def get(self,request):
        tweets = []
        for tweet in Tweet.select():
            tweets.append({ "message": tweet.message, "created": tweet.created, "is_published": tweet.is_published})
        return response.json(tweets)

    async def post(self,request):
        post = request.json
        insert = Tweet.create(user = 1, message = post['message'])
        insert.save()
        return response.json({'message':'Tweet created successfully', 'status' : 201})


app.add_route(UserList.as_view(), '/')

app.add_route(TweetList.as_view(), '/tweet')

app.run(host = "0.0.0.0", port = 8000, debug = True)
