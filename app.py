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

    # 3. Fetch Movies
    cur = mysql.connection.cursor()
    # Note: 'movies.genre' hata diya hai safety ke liye
    cur.execute("""
        SELECT shows.id, movies.title, movies.poster, shows.price, shows.show_time
        FROM shows
        JOIN movies ON shows.movie_id = movies.id
        WHERE DATE(shows.show_time) = %s
        ORDER BY shows.show_time ASC
    """, (selected_date_str,))
    
    raw_data = cur.fetchall()



    # 4. Process Data
    movies_data = []
    for m in raw_data:
        dt_obj = m[4] 
        if isinstance(dt_obj, str): 
            dt_obj = datetime.strptime(dt_obj, '%Y-%m-%d %H:%M:%S')
            
        formatted_time = dt_obj.strftime("%I:%M %p") 

        movies_data.append({
            'show_id': m[0],
            'title': m[1],
            'poster': m[2],
            'genre': 'Blockbuster', 
            'price': m[3],
            'time': formatted_time
        })

    return render_template('movies.html', movies=movies_data, date_tabs=date_tabs)





@app.route('/lock_seats', methods=['POST'])
def lock_seats():
    data = request.json
    show_id = data['show_id']
    seats = data['seats']

    cur = mysql.connection.cursor()

    for seat in seats:
        cur.execute("""
            UPDATE seats
            SET status='locked', lock_time=NOW()
            WHERE show_id=%s AND seat_number=%s AND status='available'
        """, (show_id, seat))

        if cur.rowcount == 0:
            return jsonify({"status":"failed"})


    mysql.connection.commit()
    session['locked_seats'] = seats
    session['show_id'] = show_id

    return jsonify({"status":"ok"})