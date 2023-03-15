# flask minimal app
from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
@app.route('/User Login')
def index1():
    return render_template('User Login.html')
@app.route('/User Signup')
def index2():
    return render_template('User Signup.html')
@app.route('/Blood Donation Camp')
def index3():
    return render_template('Blood Donation Camp.html')
@app.route('/Blood Availability Search')
def index4():
    return render_template('Blood Availability Search.html')
def index():
    return render_template('index.css')
# make a flask file executable
if __name__ == "__main__":
    app.run(debug=True)
