#This is the service.py file
from flask import Flask, make_response, request
from functools import wraps
import requests

#Using flasks for front end micro enviroment
app = Flask(__name__)

#Authetication feature that requires user to login to have access
def auth_required(f):
    #functool to allow wrappers
    @wraps(f)
    #username function using request with flask
    def decorated(*args, **kwargs):
        auth = request.authorization
        #Grants access with right username and password
        if auth and auth.username == secr.serv_user and auth.password == secr.serv_pass:
            return f(*args, **kwargs)
        #Failed user and pass
        else:
            return make_response('Could not verify your login.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated

#Creating the main directory for the website
@app.route('/')
@auth_required
def index():
    return "Main Directory"


#Runs the application of Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)