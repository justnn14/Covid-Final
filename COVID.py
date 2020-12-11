#This is the service.py file
from flask import Flask, make_response, request, redirect, render_template, url_for, flash
from functools import wraps
import covidAssessment as ca
import requests
import pandas as pd
import json
import pymongo

#Using flasks for front end micro enviroment
app = Flask(__name__)

#Defining the mongodb within each session
def init_db():
    #Creating a dict within database, then info collection
    client = pymongo.MongoClient()
    db = client['database']
    collection = db["info"]
    #resets collection
    collection.drop() #drops
    collection = db["info"] #remake
    mydict = { "Testing Recommendation numbers: ": 0, "Quarantine Recommendation numbers: ": 0, "No need for quarantine or testing: ": 0}
    collection.insert_one(mydict)    #adding dict to info collection

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

#Creating the main directory for the website, sends you
@app.route('/', methods=["GET", "POST"])
def index():
    #If a get method, take the main page for website
    if request.method == 'GET':
        return render_template('main.html')
    #If post method, allow user to enter method of entering
    if request.method == 'POST':
        link = request.form.get('link')
        if link == '1':
            return redirect(url_for('selfTest'))
        elif link == '2':
            return redirect(url_for('covidTips'))
        elif link == '3':
            return redirect(url_for('inputAddress'))
        else:
            return """Make sure to add form data value to choose redicted link.
                  link==1 - Feeling sick? Take a self-assessment test for Covid-19.
                  link==2 - Pandemics can be stressful. Learn some coping techniques here.
                  link==3 - Want to a Covid-19 test? Find your nearest testing center here."""


# Routes user to Self-User Assessment contain a series of questions
@app.route('/Self-Test')
def selfTest():
    #renders the page to allow answering questions for self test
    return render_template('quiz.html', q = ca.only_questions, o = ca.test_questions, cq = ca.contact_question)

# This is called after the submit button is pressed on the UI
@app.route('/post-assessment', methods=['GET', 'POST'])
def postAssessment():
    needQuarantine = False
    needTesting = False
    closeContact = False
    
    for i in ca.only_questions:
        if i == ca.contact_question:
            value = request.form.get(i)
            if value == ca.test_questions[i][0]:
                closeContact = True
                if needQuarantine:
                    needTesting = True
                else:
                    needQuarantine = True
        else:
            values = request.form.getlist(i)
            if len(values) > 0:
                if i == ca.moderate_check:
                    needQuarantine = True
                if i == ca.extreme_check:
                    needTesting = True
            
    if needTesting == True:
        needQuarantine = True


    #Accessing MongoDB
    client = pymongo.MongoClient()
    db = client['database']
    collection = db["info"]
    if needTesting:
        #Add to testing Count
        testDBResults = collection.find_one()
        myquery = { "Testing Recommendation numbers: ": testDBResults["Testing Recommendation numbers: "]}
        newvalues = { "$set": { "Testing Recommendation numbers: ": testDBResults["Testing Recommendation numbers: "]+1} }
        collection.update_one(myquery, newvalues)
    if needQuarantine:
        #Add to quarantine Count
        testDBResults = collection.find_one()
        myquery = { "Quarantine Recommendation numbers: ": testDBResults["Quarantine Recommendation numbers: "]}
        newvalues = { "$set": { "Quarantine Recommendation numbers: ": testDBResults["Quarantine Recommendation numbers: "]+1} }
        collection.update_one(myquery, newvalues)
    if not needQuarantine and not needTesting:
        #Updating number for dont need quarantine or testing
        testDBResults = collection.find_one()
        myquery = { "No need for quarantine or testing: ": testDBResults["No need for quarantine or testing: "]}
        newvalues = { "$set": { "No need for quarantine or testing: ": testDBResults["No need for quarantine or testing: "]+1} }
        collection.update_one(myquery, newvalues)
    #Renders the page for results
    return render_template('quizResults.html', goTest = needTesting, goQuarantine = needQuarantine, contact = closeContact )


# Creating CovidTips
@app.route('/Covid-Coping-Tips')
def covidTips():
    #Url of the Tips    
    return render_template('covidTips.html')


#directory to ask user to input address
@app.route('/input-address/', defaults={'error': None})
@app.route('/input-address/<error>')
def inputAddress(error):
    #when no error, ask user to input address
    if not error:
        return render_template('inputAddy.html')
    #when error from bad address, ask user to enter a more distingushable address
    else:
        return render_template('inputAddy.html', error=error)

#post methodolgy for entering the input address
@app.route('/input-address/', defaults={'error': None}, methods=['POST'])
@app.route('/input-address/<error>', methods=['POST'])
def inputAddressPost(error):
    #When information is submmiteed and valid address, redirects user to nearby test
    addressText = request.form['addressText']
    return redirect(url_for('nearbyTest', address=addressText))

#Routing to Testing Center Module
@app.route('/Testing-Near-You/<address>')
def nearbyTest(address):
    #API keys for google maps and covid testing location
    google_key = 'AIzaSyClhso0F8EGlvG3C2c_NyKegTH6_fVabV8'
    covid_key = '_HJsegSQUeUVqvKlgw9qySkKieJdc9n7lw5uMVn6FtM'
    
    #using google maps api to get geographic coordinates from an address
    google_maps = json.loads((requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + google_key)).text)
    
    #if there is no coordinates for that address return an error message
    if(len(google_maps['results']) == 0) :
        return redirect(url_for('inputAddress') + "Bad Address. Please try again with a more distinguishable address.")
    
    #initializing latitude and longitude from google maps data
    lat = google_maps['results'][0]['geometry']['location']['lat']
    lng = google_maps['results'][0]['geometry']['location']['lng']

    #using covid testing api to get closest testing location
    covid = json.loads((requests.get('https://discover.search.hereapi.com/v1/discover?apikey=' + covid_key + '&q=Covid&at=' + str(lat) + ',' + str(lng) + '&limit=3')).text)
    addy = covid['items'][0]['address']['label']
    split_addy = addy.split(':')

    #going to new page with results for testing location search
    return render_template('foundAddy.html', fromAddy=address, toAddy=split_addy[1])

#Routing to Admin Module
@app.route('/admin')
@auth_required
def admin():
    #Accessing mongoDB
    client = pymongo.MongoClient()
    db = client['database']
    collection = db["info"]
    #Obtain Results
    testDBResults = collection.find_one()
    test = testDBResults["Testing Recommendation numbers: "]
    quar = testDBResults["Quarantine Recommendation numbers: "]
    nothing = testDBResults["No need for quarantine or testing: "]
    #Showcasing Results to Admin ONLY
    return "Total recommended to get a test: " + str(test) + "<br />Total recommended to quarantine: " + str(quar) + "<br />Total recommended to do nothing: " \
            + str(nothing) + "<br />Total self assesment takers: " + str(quar + nothing)

#Runs the application of Flask
if __name__ == '__main__':
    init_db() #Init Database
    app.run(debug=True, port=5000) # runs the app