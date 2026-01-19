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
