from flask import *
from flask_bootstrap import Bootstrap
import psycopg2
import psycopg2.extras
import hashlib

app = Flask(__name__)
app.secret_key="veryverypublic"
Bootstrap(app)

connect = psycopg2.connect("dbname=sugang user=postgres password=0000 client_encoding=utf8")
cur = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

#@app.route('/program/<name>')
#def program(name):
#    return render_template('bootstrap.html', name=name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('mainpage.html')

@app.route('/mycourses')
def mycourses():
    return render_template('mycourses.html')

@app.route('/allcourses')
def allcourses():
    cur.execute('SELECT * FROM course, section WHERE course.course_id=section.course_id;')
    result=cur.fetchall()
    modified=result.copy()
    for i in range(len(result)):
        cur.execute('SELECT * FROM section_time JOIN timeslot ON section_time.timeslot_id=timeslot.id;')
        temp=cur.fetchall()
        modified[i]['timeslot']=''
        for j in temp:
            modified[i]['timeslot']+=j['day']+'요일 '+j['period']+'교시\n'
        modified[i]['timeslot']=modified[i]['timeslot'].rstrip()
    return render_template('allcourses.html', courses=modified)

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

@app.route('/changepw', methods=['GET', 'POST'])
def changepw():
    if request.method=='POST':
        password = request.form['pw']
        cur.execute(
            "UPDATE login SET pw='%s';" % hashlib.sha512(password.encode()).hexdigest()
        )
        cur.commit()
        flash('Updated')
    return render_template('changepw.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        id = request.form['id']
        password = request.form['password']
        print(id, password)

        cur.execute(
            "SELECT * FROM login WHERE id='%s' AND pw='%s';" % (id, hashlib.sha512(password.encode()).hexdigest()))
        result = cur.fetchall()
        if len(result) != 1:
           flash('No Matching Information')
           return render_template('login.html')
        else:
           return render_template('mainpage.html', user=result[0]['id'])
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    id = request.form['id']
    password = request.form['password']

    cur.execute(
        "UPDATE login SET pw='%s';" %(password)
    )

if __name__ == '__main__':
    app.run()