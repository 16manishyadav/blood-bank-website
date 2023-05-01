# flask minimal app
from flask import Flask,render_template,session,redirect,url_for,flash,request
import pyrebase
from markupsafe import Markup
app = Flask(__name__)
config = { 'apiKey': "AIzaSyAyUFlVUHj8VYiVMasc8L7aoOvN8jVsuqs",
           'authDomain': "blood-bank-website.firebaseapp.com",
           'projectId': "blood-bank-website",
           'storageBucket': "blood-bank-website.appspot.com",
           'messagingSenderId': "3264708451",
           'appId': "1:3264708451:web:cac92bcc5164edcacb5d56",
           'measurementId': "G-XLW77GHD52",
           'databaseURL' : "https://blood-bank-website-default-rtdb.firebaseio.com"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()
db = firebase.database()
app.secret_key = 'secret'

# app route for BloodManager page
@app.route('/',methods=['GET','POST'])
def index6():
    if request.method == 'POST':
        # get form data
        id = request.form['id']
        name = request.form['name']
        state = request.form['state']
        city = request.form['city']
        contact = request.form['contact']
        Aplus = request.form['A+']
        Aminus = request.form['A-']
        Bplus = request.form['B+']
        Bminus = request.form['B-']
        ABplus = request.form['AB+']
        ABminus = request.form['AB-']
        Oplus = request.form['O+']
        Ominus = request.form['O-']
        datetime = request.form['datetime']
        # store data in database
        data = {"name":name,"state":state,"city":city,"contact":contact,"A+":Aplus,"A-":Aminus,"B+":Bplus,"B-":Bminus,"AB+":ABplus,"AB-":ABminus,"O+":Oplus,"O-":Ominus,"datetime":datetime}
        # if id does not exist in database
        if db.child("bloodbank").child(id).get().val() == None:
            db.child("bloodbank").child(id).set(data)
            # make a markup object to display the data added successfully message
            flash("Blood Bank Added Successfully")
        # if id already exists in database update the data
        else:
            db.child("bloodbank").child(id).update(data)
            flash("Blood Bank Updated Successfully")
        # return render_template('BloodManager.html')
    return render_template('BloodManager.html')

# app route for Blooddonationmanager page
@app.route('/Blooddonationmanager',methods=['GET','POST'])
def index7():
    if request.method == 'POST':
        # get form data
        id = request.form['id']
        state = request.form['state']
        city = request.form['city']
        contact = request.form['contact']
        date = request.form['date']
        time = request.form['time']
        address = request.form['address']
        # store data in database
        data = {"state":state,"city":city,"contact":contact,"date":date,"time":time,"address":address}
        # if id does not exist in database
        if db.child("camp").child(id).get().val() == None:
            db.child("camp").child(id).set(data)
            # make a markup object to display the data added successfully message
            flash("Blood Donation Camp Added Successfully")
        # if id already exists in database update the data
        else:
            db.child("camp").child(id).update(data)
            flash("Blood Donation Camp Updated Successfully")
        # return render_template('Blooddonationmanager.html')
    return render_template('Blooddonationmanager.html')

# make a flask file executable
if __name__ == "__main__":
    app.run(debug=True)



        

