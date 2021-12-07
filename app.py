import requests
from flask import *
from flask_bootstrap import Bootstrap
import psycopg2
import psycopg2.extras
import hashlib

app = Flask(__name__)
app.secret_key = "veryverypublic"
Bootstrap(app)

connect = psycopg2.connect("dbname=termproject user=postgres password=wkdrnwkdrn1@ client_encoding=utf8")
cur = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


# @app.route('/program/<name>')
# def program(name):
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


@app.route('/allcourses', methods=['GET', 'POST'])
def allcourses():
    query = 'SELECT * FROM section JOIN instructor ON section.instructor_id=instructor.instructor_id, course JOIN department ON course.dept_name=department.college_name WHERE course.course_id=section.course_id'
    if request.method == 'POST':
        year = request.form['pYear']
        semester = request.form['pTerm']
        college = request.form['pCol']
        credit = request.form['pCredit']
        instructor = request.form['pProf']
        # TODO
        if year != '':
            query += " AND section.year=%d" % int(year)
        if semester != '':
            query += " AND section.semester='%s'" % semester
        if college != '':
            if college=='교양':
                query+=" AND course.type='elective'"
            else:
                query+=" AND course.type<>'elective' AND course.dept_name='%s'"%college
        if credit != '':
            query+=" AND course.credit=%d"%credit
        if instructor != '':
            query+=" AND section.instructor_name='%s'"%instructor
    query+=' ORDER BY course_id, section_id ASC;'
    cur.execute(query)
    result = cur.fetchall()
    modified=[]
    for i in result:
        query2="SELECT * FROM section_time JOIN timeslot ON section_time.timeslot_id=timeslot.id WHERE section_id='%s'"%i['id']
        if request.method == 'POST':
            day = request.form['pDay']
            time = request.form['pStartTime']
            if day!='':
                query2+=" AND day='%s'"%day
            if time!='':
                query2+=" AND period=%d"%int(time)
        query2+=' ORDER BY timeslot_id ASC;'
        cur.execute(query2)
        temp=cur.fetchall()
        if len(temp)>0:
            modified.append(i)
            modified[-1]['timeslot']=''
            for j in temp:
                modified[-1]['timeslot']+=j['day']+' '+j['period']+'교시\n'
            modified[-1]['timeslot']=modified[-1]['timeslot'].rstrip()
    return render_template('allcourses.html', courses=modified)


@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    # TODO
    # 학생 개인정보 가져오는 쿼리 짜야함.
    cur.execute(
        "SELECT * FROM "
    )

    # 탈퇴 버튼 누를 시
    # login정보 삭제
    if request.method == 'POST':
        std_id = request.form['std_id']
        cur.execute(
            "DELETE FROM login WEHRE std_id = '%s';" % (std_id)
        )
        return render_template('login.html')

    return render_template('mypage.html')


@app.route('/changepw', methods=['GET', 'POST'])
def changepw():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['pw']
        cur.execute(
            "UPDATE login SET pw='%s' WHERE id = '%s';" % (hashlib.sha512(password.encode()).hexdigest(), id)
        )
        return render_template('login.html')

        cur.commit()
        flash('Updated')

    return render_template('changepw.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        print(id, password)

        cur.execute(
            "SELECT * FROM login WHERE id='%s' AND pw='%s';" % (id, hashlib.sha512(password.encode()).hexdigest()))
        result = cur.fetchall()
        if len(result) != 1:
            flash('No Matching Information')
            return render_template('login.html')
        elif id == 'admin':
            return render_template('admin.html', user=result[0]['id'])
        else:
            return render_template('mainpage.html', user=result[0]['id'])

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    id = request.form['id']
    password = request.form['password']

    cur.execute(
        "UPDATE login SET pw='%s';" % hashlib.sha512(password.encode()).hexdigest()
    )


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # TODO
    # 기본 검색 기능은 일반 유저와 동일하게 가능하도록.

    if request.method == 'POST':
        if request.form.get('submit') == "submit":
            # TODO
            # 과목 추가 기능
            course_id = request.form['course_id']
            section_id = request.form['section_id']
            course_name = request.form['course_name']
            dept_name = request.form['dept_name']
            type = request.form['type']
            credits = request.form['credits']
            hour = request.form['hour']
            year = request.form['year']
            semester = request.form['semeseter']
            instructor_id = request.form['instructor_id']

            cur.execute(
                "INSERT INTO course VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (
                    course_id, course_name, dept_name, type, credits, hour)
            )
            cur.execute(
                "INSERT INTO section VALUES ('%s','%s','%s','%s','%s','%s');" % (
                    "DEFAULT", course_id, section_id, year, semester, instructor_id)
            )

        elif request.form.get('delete') == "delete":
            # 과목 삭제 기능
            dcourse_id = request.form['dcourse_id']
            dyear = request.form['dyear']
            dsemester = request.form['dsemester']
            dsection_id = request.form['dsection_id']

            cur.execute()


    return render_template('admin.html')


if __name__ == '__main__':
    app.run()
