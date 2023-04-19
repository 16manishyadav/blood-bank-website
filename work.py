# flask minimal app
import datetime
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

# app.secret_key = 'secret'

#storage
# filepath = input("Enter the file path: ")
# cloudfilepath = input("Enter the cloud file path: ")
# storage.child(cloudfilepath).put(filepath)

# print(storage.child(cloudfilepath).get_url(None))

# cloudfilepath = input("Enter the cloud file path: ")
# storage.child(cloudfilepath).download("","")

#solve urllib error
# import urllib.request
# #reading file
# cloudfilepath = input("Enter the cloud file path: ")
# url = storage.child(cloudfilepath).get_url(None)
# f = urllib.request.urlopen(url).read()
# print(f)

#database



db = firebase.database()

class bloodbank:
    def __init__(self,id):
        self.id=id
        self.name=None
        self.state=None
        self.city=None
        self.contact=None
        self.Aplus=None
        self.Aminus=None
        self.Bplus=None
        self.Bminus=None
        self.ABplus=None
        self.ABminus=None
        self.Oplus=None
        self.Ominus=None
        self.datetime=None
        #check if id exists
        if db.child("bloodbank").child(self.id).get().val() is None:
            self._add()
    def _add(self):
        #take inputs
        self.name = input("Enter the name of the blood bank: ")
        self.state = input("Enter the state of the blood bank: ")
        self.city = input("Enter the city of the blood bank: ")
        self.contact = input("Enter the contact number of the blood bank: ")
        self.Aplus = input("Enter the number of A+ blood bags available: ")
        self.Aminus = input("Enter the number of A- blood bags available: ")
        self.Bplus = input("Enter the number of B+ blood bags available: ")
        self.Bminus = input("Enter the number of B- blood bags available: ")
        self.ABplus = input("Enter the number of AB+ blood bags available: ")
        self.ABminus = input("Enter the number of AB- blood bags available: ")
        self.Oplus = input("Enter the number of O+ blood bags available: ")
        self.Ominus = input("Enter the number of O- blood bags available: ")
        self.datetime = input("Enter the date and time of the blood bank: ")
        #push to database with id
        data = {"name":self.name,"state":self.state,"city":self.city,"contact":self.contact,"A+":self.Aplus,"A-":self.Aminus,"B+":self.Bplus,"B-":self.Bminus,"AB+":self.ABplus,"AB-":self.ABminus,"O+":self.Oplus,"O-":self.Ominus,"datetime":self.datetime}
        #set data
        db.child("bloodbank").child(self.id).set(data)
    def update(self):
        #take input if not given then keep previous value
        self.name = input("Enter the name of the blood bank: ")
        self.state = input("Enter the state of the blood bank: ")
        self.city = input("Enter the city of the blood bank: ")
        self.contact = input("Enter the contact number of the blood bank: ")
        self.Aplus = input("Enter the number of A+ blood bags available: ")
        self.Aminus = input("Enter the number of A- blood bags available: ")
        self.Bplus = input("Enter the number of B+ blood bags available: ")
        self.Bminus = input("Enter the number of B- blood bags available: ")
        self.ABplus = input("Enter the number of AB+ blood bags available: ")
        self.ABminus = input("Enter the number of AB- blood bags available: ")
        self.Oplus = input("Enter the number of O+ blood bags available: ")
        self.Ominus = input("Enter the number of O- blood bags available: ")
        self.datetime = input("Enter the date and time of the blood bank: ")

        #update database    
        data = {"name":self.name,"state":self.state,"city":self.city,"contact":self.contact,"A+":self.Aplus,"A-":self.Aminus,"B+":self.Bplus,"B-":self.Bminus,"AB+":self.ABplus,"AB-":self.ABminus,"O+":self.Oplus,"O-":self.Ominus,"datetime":self.datetime}
        db.child("bloodbank").update(data)

class reader:
    def __init__(self,state,city,bloodgroup):
        self.state=state
        self.city=city
        self.bloodgroup=bloodgroup
    def read(self):        
        bloodbanks = db.child("bloodbank").order_by_child("state").equal_to(self.state).get()
        # print(bloodbanks.val())
        for bloodbank in bloodbanks.each():
            data = bloodbank.val()
            if data[self.bloodgroup]!="0" and data["city"]==self.city:
                print(data["name"])
                print(data["contact"])
                print(data["datetime"])
                print(self.bloodgroup,data[self.bloodgroup])

        
#making a class for blood donation camp and its variable are state , city , date, contact, address,time.
class camp:
    def __init__(self,id):
        self.id=id
        self.state=None
        self.city=None
        self.date=None
        self.contact=None
        self.address=None
        self.time=None
        #check if id exists
        if db.child("camp").child(self.id).get().val() is None:
            self._add()
    def _add(self):
        #take inputs
        self.state = input("Enter the state of the blood camp: ")
        self.city = input("Enter the city of the blood camp: ")
        self.date = input("Enter the date of the blood camp: ")
        self.contact = input("Enter the contact number of the blood camp: ")
        self.address = input("Enter the address of the blood camp: ")
        self.time = input("Enter the time of the blood camp: ")
        #push to database with id
        data = {"state":self.state,"city":self.city,"date":self.date,"contact":self.contact,"address":self.address,"time":self.time}
        #set data
        db.child("camp").child(self.id).set(data)
    def update(self):
        #take input if not given then keep previous value
        self.state = input("Enter the state of the blood camp: ")
        self.city = input("Enter the city of the blood camp: ")
        self.date = input("Enter the date of the blood camp: ")
        self.contact = input("Enter the contact number of the blood camp: ")
        self.address = input("Enter the address of the blood camp: ")
        self.time = input("Enter the time of the blood camp: ")
        #update database    
        data = {"state":self.state,"city":self.city,"date":self.date,"contact":self.contact,"address":self.address,"time":self.time}
        db.child("camp").update(data)

#create a function to update the database
def update():
    #take input
    id = input("Enter the id of the blood bank: ")
    #check if id exists
    if db.child("bloodbank").child(id).get().val() is None:
        print("Blood bank does not exist")
    else:
        #create object
        bloodbank = bloodbank(id)
        #update
        bloodbank.update()

class campreader:
    def __init__(self,state,city):
        self.state=state
        self.city=city
    def read(self):        
        camps = db.child("camp").order_by_child("state").equal_to(self.state).get()
        for camp in camps.each():
            data = camp.val()
            if data["city"]==self.city:
                print(data["date"])
                print(data["time"])
                print(data["address"])
                print(data["contact"])
    


