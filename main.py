from datetime import time

import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import firestore
import flask
from flask import request, jsonify, Flask, render_template

# initialize firebase application
#firebase_admin.initialize_app()
cred = credentials.Certificate('testing-bf5a4-firebase-adminsdk-k3wvf-9481825d20.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testing-bf5a4.firebaseio.com/'
})

db = firestore.client()

# connect to db
db = firestore.client()

app = Flask(__name__)
# global variables
recData = {'domain': "google",
           'city': "Bangalore",
           'email': "xyz@gmail.com",
           'name': "Unknown",
           'mobile': "7795824685",
           'gender': "Male",
           'dob': "11-08-1997",
           'nationality': "India"
           }

@app.route('/',  methods =["GET", "POST"])
def hello_world():
  if request.method == "POST":
    #recData = flask.request.json
    #city = recData['city']
    #email = recData['email']
    #name = recData['name']
    #mobile = recData['mobile']  
    #gender = recData['gender']
    #dob = recData['dob']
    #nationality = recData['nationality']
    city = request.form.get("city") 
    email = request.form.get("email") 
    name = request.form.get("name") 
    mobile = request.form.get("mobile")   
    gender = request.form.get("gender") 
    dob = request.form.get("dob") 
    nationality = request.form.get("nationality") 
    domain = request.form.get("domain") 
    
    docref = db.collection('Profile').document()
    data1 = {
           'city': city,
           'email': email,
           'name': name,
           'mobile': mobile,
           'gender': gender,
           'dob': dob,
           'nationality': nationality
         }
    docref.set(data1)
    type = ''
    ldoc_id = docref.id
    if domain == 'mobile' or domain == 'email':
         type += "communication"
    elif domain == 'facebook' or domain == 'github' or domain == 'linkedin':
         type += "social"
        
    data = {
           'type': type
           'city': city,
           'email': email,
           'name': name,
           'mobile': mobile,
           'gender': gender,
           'dob': dob,
           'nationality': nationality
         }
             
    lpvstatus = 'True'
    resp = requests.post('https://us-central1-folk-dev-com-db.cloudfunctions.net/createLinkedProfile',json=data)
     
    #return jsonify(data)
    return 'your name is: ' + name
  return render_template("index.html") 


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
