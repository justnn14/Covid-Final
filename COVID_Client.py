from flask import Flask, request
from functools import wraps
import requests
from bs4 import BeautifulSoup

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
        if auth and auth.username == "malvincejust" and auth.password == "Netapp23":
            return f(*args, **kwargs)
        #Failed user and pass
        else:
            return make_response('Could not verify your login.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated

#Routing to Admin Module client
@app.route('/admin', methods=['GET'])
@auth_required
def admin():  
    #Can pass authroization through hardcode, since you needed be authticated to use this route.
    req = requests.get('http://127.0.0.1:5000/admin', auth=("malvincejust", "Netapp23"))
    return str(req.text)

#Main director of client
@app.route('/', methods=["GET", "POST"])
def index():
    #If a get method, take the main page for website
    if request.method == 'GET':
        req = requests.get('http://127.0.0.1:5000/')
        return str(req.text)
    #If post method, allow user to enter method of entering
    if request.method == 'POST':
        link = request.form.get('link')
        newCombo = {'link': link}
        post = requests.post('http://127.0.0.1:5000/', data=(newCombo))
        return str(post.text)

# Accessing the Self-Assessment
# Return the Self-Assessment as a Text to the Client
@app.route('/Self-Test', methods=['GET'])
def selfTest():
    if request.method == 'GET':
        # Printing out the Text of the Self-Assessment
        req = requests.get('http://127.0.0.1:5000/Self-Test')
        htmlExtract = req.text
        
        # Utilize BeautifulSoup4 as an HTML text to string converter so that cmd line output is more 'readable'
        soup = BeautifulSoup(htmlExtract)
        return str(soup.get_text())
        
# Creating CovidTips
@app.route('/Covid-Coping-Tips', methods=['GET'])
def covidTips():
    #Url of the Tips    
    if request.method == 'GET':
        req = requests.get('http://127.0.0.1:5000/Covid-Coping-Tips')
        htmlExtract = req.text
        
        # Utilize BeautifulSoup4 as an HTML text to string converter so that cmd line output is more 'readable'
        soup = BeautifulSoup(htmlExtract)
        return str(soup.get_text())

#Post method to get address
@app.route('/input-address/', methods=["GET", "POST"])
def inputAddress():
    if request.method == 'GET':
        return "This is a Post method only, post the address in data. Ex: address='address'"
    if request.method == 'POST':
        #obtain from data
        address = request.form['address']
        req = requests.get('http://127.0.0.1:5000/Testing-Near-You/' + str(address))
        soup = BeautifulSoup(req.text)
        return str(soup.get_text())
        
#Routing to Testing Center Module
@app.route('/Testing-Near-You/<address>', methods=["GET"])
def nearbyTest(address):
    req = requests.get('http://127.0.0.1:5000/Testing-Near-You/' + str(address))
    soup = BeautifulSoup(req.text)
    return str(soup.get_text())
        
#Runs the application of Flask
if __name__ == '__main__':
    app.run(debug=True, port=5001) # runs the app