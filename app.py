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

def outputer(name,contact,datetime,bloodgroup,quantity):
        data = Markup('<tr> <td>'+name+'</td> <td>'+contact+'</td> <td>'+datetime+'</td> <td>'+bloodgroup+'</td> <td>'+quantity+'</td> </tr>')
        return data

class reader:
        def __init__(self,state,city,bloodgroup):
            self.state=state
            self.city=city
            self.bloodgroup=bloodgroup
        def read(self):        
            bloodbanks = db.child("bloodbank").order_by_child("state").equal_to(self.state).get()
            final_output=""
            for bloodbank in bloodbanks.each():
                data = bloodbank.val()
                if data[self.bloodgroup]!="0" and data["city"]==self.city:
                    final_output+=outputer(data["name"],data["contact"],data["datetime"],self.bloodgroup,data[self.bloodgroup])
            return final_output
        
def outputer_camp(address,contact,date,time):
    data = Markup('<tr> <td>'+address+'</td> <td>'+contact+'</td> <td>'+date+'</td> <td>'+time+'</td> </tr>')
    return data

class reader_camp:
    def __init__(self,state,city):
        self.state=state
        self.city=city
    def read(self):        
        camps = db.child("camp").order_by_child("state").equal_to(self.state).get()
        final_output=""
        for camp in camps.each():
            data = camp.val()
            if data["city"]==self.city:
                final_output+=outputer_camp(data["address"],data["contact"],data["date"],data["time"])
        return final_output

@app.route("/")
def index():
    if 'user' in session:
        log = Markup('<a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"> Logined ' + '</a> <ul class="dropdown-menu"> <li><a class="dropdown-item" href="http://127.0.0.1:5000/logout">User Logout</a></li>')
    else:
        log = Markup('<a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"> Login/Signup </a> <ul class="dropdown-menu"> <li><a class="dropdown-item" href="http://127.0.0.1:5000/User%20Login">User Login</a></li> <li> <hr class="dropdown-divider"> </li> <li><a class="dropdown-item" href="http://127.0.0.1:5000/User%20Signup">User Signup</a></li> </ul>')
    return render_template('index.html',logger=log)
@app.route('/User Login', methods=['POST','GET'])
def login():
    
    if 'user' in session:
        return index()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            loggedin = True
            return redirect(url_for('index'))
        except:
            session.pop('user', None)
            return render_template('User Login.html',alreadyuser = Markup('<div class="alert alert-danger alert-dismissible fade show" role="alert"> <strong> Login failed) </strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div>'))
    return render_template('User Login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    # create markup object for notification as logout successful
    notification = Markup('<div class="alert alert-success alert-dismissible fade show" role="alert"> <strong> Logout successful </strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div>')
    return render_template('User Login.html',notification=notification)
@app.route('/User Signup', methods=['POST','GET'])
def signup():
    # create markup object for notification as signup successful
    notification = Markup('<div class="alert alert-success alert-dismissible fade show" role="alert"> <strong> Signup successful </strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div>')
    # create markup object for notification as signup failed check password and confirm password
    notification2 = Markup('<div class="alert alert-danger alert-dismissible fade show" role="alert"> <strong> Signup failed Check Password and Confirm Password </strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div>')
    # notification2 = Markup('<div class="alert alert-danger alert-dismissible fade show" role="alert"> <strong> Signup failed </strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div>')
    # create markup object for notification as user already exists
    notification3 = Markup('<div class="alert alert-danger alert-dismissible fade show" role="alert"> <strong> User already exists </strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div>')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if confirm_password == password:
            try:
                auth.create_user_with_email_and_password(email, password)
                # print("Signup successful")
                return render_template('User Login.html',notification=notification)
            except:
                # print("User already exists")
                return render_template('User Login.html',notification=notification3)
        else:
            return render_template('User Signup.html',notification=notification2)
            # print("Signup failed")
    return render_template('User Signup.html')
@app.route('/Blood Donation Camp',methods=['POST','GET'])
def index3():
    # make markup object for notification
    notification = Markup('<div class="alert alert-danger alert-dismissible fade show" role="alert"> <strong> Please login first </strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div>')
    # if user not in session than redirect to login page and print message "Please login first"
    if 'user' not in session:
        return render_template('User Login.html',notification=notification)
    output = ""
    if request.method == 'POST':
        state = request.form.get('state')
        city = request.form.get('city')
        data = reader_camp(state,city)
        output = data.read()
        if(output==""):
            output = Markup('<tr> <td colspan="5">No data found</td> </tr>')
        return render_template('Blood Donation Camp.html',output=output)
    return render_template('Blood Donation Camp.html',output=output)
@app.route('/Blood Availability Search',methods=['POST','GET'])
def index4():
    notification = Markup('<div class="alert alert-danger alert-dismissible fade show" role="alert"> <strong> Please login first </strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div>')
    # if user not in session than redirect to login page and print message "Please login first"
    if 'user' not in session:
        return render_template('User Login.html',notification=notification)
    final_output = ""
    if request.method == 'POST':
        bloodgroup = request.form.get('bloodgroup')
        city = request.form.get('city')
        state = request.form.get('state')
        data = reader(state,city,bloodgroup)
        final_output = data.read()
        if(final_output==""):
            # final_output = Markup('<strong>No data found</strong>')
            # make final output as NO DATA FOUND make this as a markup object and allign it to center 
            final_output = Markup('<div class="container"> <div class="row"> <div class="col-md-12"> <div class="alert alert-danger alert-dismissible fade show" role="alert"> <strong>Invalid Inputs No Data</strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> </div> </div> </div> </div>')
        return render_template('Blood Availability Search.html',final_output=final_output)
    return render_template('Blood Availability Search.html',final_output=final_output)

# app route for User Help page
@app.route('/User Help')
def index5():
    if 'user' in session:
        log = Markup('<a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"> Logined ' + '</a> <ul class="dropdown-menu"> <li><a class="dropdown-item" href="http://127.0.0.1:5000/logout">User Logout</a></li>')
    else:
        log = Markup('<a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"> Login/Signup </a> <ul class="dropdown-menu"> <li><a class="dropdown-item" href="http://127.0.0.1:5000/User%20Login">User Login</a></li> <li> <hr class="dropdown-divider"> </li> <li><a class="dropdown-item" href="http://127.0.0.1:5000/User%20Signup">User Signup</a></li> </ul>')
    return render_template('User Help.html',logger=log)

# make a flask file executable
if __name__ == "__main__":
    app.run(debug=True)




        

