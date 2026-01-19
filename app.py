from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config.from_pyfile('config.py')

mysql = MySQL(app)
bcrypt = Bcrypt(app)
Session(app)

@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(
            request.form['password']
        ).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
            (name,email,password)
        )
        mysql.connection.commit()
        return redirect('/login')
    return render_template('signup.html')





@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id,password FROM users WHERE email=%s",(email,))
        user = cur.fetchone()

        if user and bcrypt.check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect('/movies')

    return render_template('login.html')


@app.route('/movies')
def movies():
    #  Get Selected Date from URL (default to Today)
    selected_date_str = request.args.get('date')
    if not selected_date_str:
        selected_date = datetime.now().date()
        selected_date_str = selected_date.strftime('%Y-%m-%d')
    else:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()


    #  Generate Next 4 Days for the Tabs
    date_tabs = []
    today = datetime.now().date()
    for i in range(4):
        date_obj = today + timedelta(days=i)
        date_tabs.append({
            'display': date_obj.strftime('%a, %d %b'), 
            'value': date_obj.strftime('%Y-%m-%d'),    
            'active': (date_obj == selected_date)      
        })