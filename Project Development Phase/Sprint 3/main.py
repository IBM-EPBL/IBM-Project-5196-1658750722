from flask import Flask,render_template,request,url_for,redirect,session,flash
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import ibm_db
from headlines import news_headlines
from headlines import news_category
from mail import *
from key_search import search_by_key


conn = ibm_db.connect(
    "DATABASE=#;HOSTNAME=#;PORT=#;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=#;PWD=#",
    '', '')

app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/',methods=['POST','GET'])
def sign_in():
    all_users=[]

    if request.method=='POST':
        user_email=request.form['email']
        user_password=request.form['password']
        session['email'] = request.form['email']
        print(user_email,user_password)
        sql = "SELECT * FROM user"
        stmt = ibm_db.exec_immediate(conn, sql)
        users = ibm_db.fetch_both(stmt)
        while users != False:
            # print ("The Name is : ",  dictionary)
            all_users.append(users)
            users = ibm_db.fetch_both(stmt)
        for user in all_users:
            if user_email == user['EMAIL']:
                if user_password == user['PASSWORD']:
                    return redirect('/home')
                else:
                    flash("Incorrect Password")
                    return render_template('sign_in.html')
            else:
                flash("Account doesn't exist")
                return render_template('sign_in.html')




    else:
        if 'email' in session:
            return redirect('/home')
        return render_template('sign_in.html')

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

@app.route('/otp',methods=['POST','GET'])
def otp():

    if request.method == 'POST':
        num_1 = request.form['box1']
        num_2 = request.form['box2']
        num_3 = request.form['box3']
        num_4 = request.form['box4']
        my_otp=num_1+num_2+num_3+num_4

        if my_otp==session['otp']:
            print(my_otp)
            print(session['otp'])
            session.pop('otp', None)
            flash("OTP Verified")
            return redirect('/choice')

        else:
            print(my_otp)
            print(session['otp'])
            session.pop('otp', None)
            flash("OTP is wrong")
            return redirect('/otp')

    else:
        session['otp'] = str(generate_number())
        send_mail(session['email'], "Otp from news tracker", session['otp'], "yes")
        email=session['email']
        return render_template('otp.html',email=email)


@app.route('/resend_otp',methods=['POST','GET'])
def resend_otp():
    return redirect('/otp')

@app.route('/home')
def home():
    sql = "SELECT * FROM user WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['email'])
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    country=account['COUNTRY']
    fav1=account['FAV1']
    fav2 = account['FAV2']
    fav3 = account['FAV3']



    title, url, urltoimage = news_headlines(country)
    c1_title,c1_url,c1_urltoimage=news_category(country,fav1)
    c2_title, c2_url, c2_urltoimage = news_category(country,fav2)
    c3_title, c3_url, c3_urltoimage = news_category(country, fav3)
    main_length=len(title)
    c1_length=len(c1_title)
    c2_length=len(c2_title)
    c3_length = len(c3_title)
    return render_template('home.html',news_title=title,url=url,urltoimage=urltoimage,
                           c1_title=c1_title,c1_url=c1_url,c1_urltoimage=c1_urltoimage,
                           c2_title=c2_title, c2_url=c2_url, c2_urltoimage=c2_urltoimage,
                           c3_title=c3_title, c3_url=c3_url, c3_urltoimage=c3_urltoimage,
                           main_length=main_length,c1_length=18,c2_length=18,
                           c3_length=18,fav1=fav1,fav2=fav2,fav3=fav3
                           )




@app.route('/search',methods=['POST','GET'])
def search():
    if request.method == 'POST':
        keyword = request.form['search']
        search_title,search_url,search_urltoimage=search_by_key(keyword)
        search_length=len(search_title)
        print(search_url)
        return render_template("search_news.html",search_length=search_length,
                               search_title=search_title,
                               search_url=search_url,search_urltoimage=search_urltoimage)


@app.route('/profile',methods=['POST','GET'])
def profile():

    if request.method=='POST':

        user_email=session['email']

        sql = "SELECT * FROM user WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, user_email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        present_choice1 = account['FAV1']
        present_choice2 = account['FAV2']
        present_choice3 = account['FAV3']

        sql="DELETE FROM user WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, user_email)
        ibm_db.execute(stmt)

        user_name = request.form['name']
        user_email = session['email']
        user_country = request.form['country']
        user_phone = request.form['phone']
        user_password = request.form['password']
        choice1 = request.form['choice1']
        choice2 = request.form['choice2']
        choice3 = request.form['choice3']

        if choice1=="0":
            choice1=present_choice1

        if choice2=="0":
            choice2=present_choice2

        if choice3=="0":
            choice3=present_choice3

        print(user_name,user_email,user_password,user_phone,choice1,choice2,choice3)

        print(present_choice1,present_choice2,present_choice3)

        insert_sql = "INSERT INTO user VALUES (?,?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, user_email)
        ibm_db.bind_param(prep_stmt, 2, user_name)
        ibm_db.bind_param(prep_stmt, 3, user_phone)
        ibm_db.bind_param(prep_stmt, 4, user_country)
        ibm_db.bind_param(prep_stmt, 5, user_password)
        ibm_db.bind_param(prep_stmt, 6, choice1)
        ibm_db.bind_param(prep_stmt, 7, choice2)
        ibm_db.bind_param(prep_stmt, 8, choice3)
        ibm_db.execute(prep_stmt)





        return redirect('/')

    user_email = session['email']
    print(user_email)
    sql = "SELECT * FROM user WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, user_email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    return render_template("profile.html",account=account)

@app.route('/choice',methods=['POST','GET'])
def choice():
    if request.method == 'POST':
        choice1 = request.form['choice1']
        choice2 = request.form['choice2']
        choice3 = request.form['choice3']

        print(choice1,choice2,choice3)

        insert_sql = "INSERT INTO user VALUES (?,?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, session['email'])
        ibm_db.bind_param(prep_stmt, 2, session['name'])
        ibm_db.bind_param(prep_stmt, 3, session['phone'])
        ibm_db.bind_param(prep_stmt, 4, session['country'])
        ibm_db.bind_param(prep_stmt, 5, session['password'])
        ibm_db.bind_param(prep_stmt, 6, choice1)
        ibm_db.bind_param(prep_stmt, 7, choice2)
        ibm_db.bind_param(prep_stmt, 8, choice3)
        ibm_db.execute(prep_stmt)

        session.pop('phone', None)
        session.pop('country', None)
        session.pop('password', None)


        return redirect('/home')





    return render_template("choice.html")


@app.route('/logout')
def logout():
    session.pop('email', None)

    return redirect('/')






if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
