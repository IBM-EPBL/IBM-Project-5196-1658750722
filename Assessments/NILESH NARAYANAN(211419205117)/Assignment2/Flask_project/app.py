from flask import Flask, render_template, request, redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3 as sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'users ' + str(self.id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signin')
def sign_in():
    return render_template('signin.html')

@app.route('/createid', methods=['GET', 'POST'])
def create_id():
    temp=0



    if request.method == 'POST':
        name = request.form['username']
        emailid = request.form['email']
        pwd = request.form['password']
        all_posts = users.query.order_by(users.date_posted).all()

        for user in all_posts:
            if emailid == user.email:
                temp=temp+1
        if temp==0:
            new_post = users(username=name, email=emailid, password=pwd)
            db.session.add(new_post)
            db.session.commit()
            return render_template("home.html")
        else:
            return render_template("userexists.html")

@app.route('/welcome')
def welcome():
    all_posts = users.query.order_by(users.date_posted).all()
    return render_template('welcome.html', posts=all_posts)

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/verifyid', methods=['GET', 'POST'])
def verify():
    if request.method=='POST':
        emailid = request.form['email']
        pwd = request.form['password']
        all_posts = users.query.order_by(users.date_posted).all()
        for user in all_posts:
            if emailid == user.email:
                if pwd == user.password:
                    print("success")
                    return render_template('home.html')
        print("Failed")
        return render_template('signin.html')

app.route('/about')
def about():
    render_template('about.html')






if __name__ == "__main__":
    app.run(debug=True)
