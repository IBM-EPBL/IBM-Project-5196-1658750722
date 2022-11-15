from flask import Flask,render_template,request,url_for,redirect,session,flash
import ibm_db
from mail import *


conn = ibm_db.connect(
    "DATABASE=#;HOSTNAME=#;PORT=#;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=#;PWD=#",
    '', '')

app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/',methods=['POST','GET'])
def sign_in():
    return "sign in"

@app.route('/sign_up',methods=['POST','GET'])
def sign_up():
    all_users = []
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        user_country = request.form['country']
        user_phone = request.form['phone']
        user_password = request.form['password']
        user_confirm_password = request.form['confirm_password']
        print(user_name,user_email,user_country,user_phone,user_password,user_confirm_password)
        sql = "SELECT * FROM user"
        stmt = ibm_db.exec_immediate(conn, sql)
        users = ibm_db.fetch_both(stmt)
        while users != False:
            # print ("The Name is : ",  dictionary)
            all_users.append(users)
            users = ibm_db.fetch_both(stmt)
        for user in all_users:
            if user_email == user['EMAIL']:
                session.pop('email', None)
                flash("Account already exist")
                return redirect("/")

        session['email'] = request.form['email']
        session['name'] = request.form['name']
        session['country'] = request.form['country']
        session['phone'] = request.form['phone']
        session['password'] = request.form['password']
        return redirect('/otp')

    else:
        return render_template('sign_up.html')

@app.route('/forget_password',methods=['POST','GET'])
def forget_password():
    if request.method == 'POST':
        user_email = request.form['email']
        print(user_email)
        sql = "SELECT PASSWORD FROM user WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, user_email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            print(account['PASSWORD'])
            pwd="<strong>PASSWORD:<strong>"+account['PASSWORD']
            send_mail(user_email, "Your password has been received",pwd,None)
            session.pop('email', None)
            flash('Your password has been sent')
            return redirect("/")
        else:
            flash("Account doesn't exist")
            return redirect('/forget_password')

    else:
        return render_template('forget_password.html')
