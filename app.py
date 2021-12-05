from flask import *
from flask_bootstrap import Bootstrap
import psycopg2
import psycopg2.extras
import hashlib

app = Flask(__name__)
Bootstrap(app)


# connect=psycopg2.connect("dbname=원하는거 user=postgres password=알아서")
# cur=connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

### Frontend ###

@app.route('/program/<name>')
def program(name):
    return render_template('bootstrap.html', name=name)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


### Backend ###

@app.route('/backend/login', methods=['POST'])
def blogin():
    id = request.form['id']
    password = request.form['password']
    print(id, password)

    connect = psycopg2.connect("dbname=students user=postgres password=0000")
    cur = connect.cursor()
    cur.execute(
        'SELECT * FROM students WHERE id=%s AND password=%s' % (id, hashlib.sha512(password.encode()).hexdigest()))
    result = cur.fetchall()
    if len(result) != 1:
       flash('No Matching Information')
       return render_template('login.html')
    else:
       return render_template('mainpage.html', user=result[0]['id'])
    return render_template('login.html')


if __name__ == '__main__':
    app.run()