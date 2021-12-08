import requests
from flask import *
from flask_bootstrap import Bootstrap
import psycopg2
import psycopg2.extras
import hashlib

app = Flask(__name__)
app.secret_key = "htmlisnotaprogramminglanguage"
Bootstrap(app)

connect = psycopg2.connect("dbname=sugang user=postgres password=0000 client_encoding=utf8")
connect.autocommit=True
cur = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
user=None

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
    global user
    query = "SELECT * FROM section JOIN instructor ON section.instructor_id=instructor.instructor_id, course JOIN department ON course.dept_name=department.dept_name, (takes JOIN login ON takes.std_id=login.std_id) AS temp WHERE course.course_id=section.course_id AND section.id=temp.section_id AND temp.id='%s'"%user
    cur.execute(query)
    result=cur.fetchall()
    return render_template('mycourses.html', courses=result)


@app.route('/allcourses', methods=['GET', 'POST'])
def allcourses():
    query = 'SELECT * FROM (section JOIN instructor ON section.instructor_id=instructor.instructor_id) AS temp1, (course JOIN department ON course.dept_name=department.dept_name) AS temp2 WHERE temp2.course_id=temp1.course_id'
    if request.method == 'POST':
        if request.form.get('submit') == "submit":
            year = request.form['pYear']
            semester = request.form['pTerm']
            college = request.form['pCol']
            credit = request.form['pCredit']
            instructor = request.form['pProf']
            course_id = request.form['pCourCd']
            section_id = request.form['pCourCls']
            course_name = request.form['pCourNm']
            # TODO
            if year != '':
                query += " AND temp1.year=%d" % int(year)
            if semester != '':
                query += " AND temp1.semester='%s'" % semester
            if college != '':
                if college=='교양':
                    query+=" AND temp2.type='elective'"
                else:
                    query+=" AND temp2.type<>'elective' AND temp2.college_name='%s'"%college
            if credit != '':
                query+=" AND temp2.credits=%d"%int(credit)
            if instructor != '':
                query+=" AND temp1.instructor_name LIKE '%%%s%%'"%instructor
            if course_id != '':
                query+=" AND temp2.course_id LIKE '%%%s%%'"%course_id
            if section_id != '':
                query+=" AND temp1.section_id LIKE '%%%s%%'"%section_id
            if course_name != '':
                query+=" AND temp2.course_name LIKE '%%%s%%'"%course_name
    query+=' ORDER BY temp1.course_id, temp1.section_id ASC;'
    cur.execute(query)
    result = cur.fetchall()
    modified=[]
    for i in range(len(result)):
        query2="SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s' ORDER BY timeslot_id ASC;"%result[i]['id']
        cur.execute(query2)
        temp=cur.fetchall()
        result[i]['timeslot']=[]
        for j in temp:
            result[i]['timeslot'].append((j['day']+' ' if j['day'] is not None else '')+(str(j['period'])+'교시 ' if j['period'] is not None else '')+(j['building']+' ' if j['building'] is not None else '')+(j['building_address']+' ' if j['building_address'] is not None else '')+(j['place_name'] if j['place_name'] is not None else ''))
    for i in result:
        query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s'" % i['id']
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
        if request.method != 'POST' or request.method == 'POST' and (day!='' or time!='') and len(temp)>0 or request.method == 'POST' and day=='' and time=='':
            modified.append(i)
    return render_template('allcourses.html', courses=modified)


@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    global user
    # 탈퇴 버튼 누를 시
    # login정보 삭제
    if request.method == 'POST':
        std_id = request.form['std_id']
        cur.execute(
            "DELETE FROM login WEHRE std_id = '%s';" % (std_id)
        )
        flash('Eliminated')
        user=None
        return render_template('login.html')
    # TODO
    # 학생 개인정보 가져오는 쿼리 짜야함.
    cur.execute(
        "SELECT * FROM student JOIN login ON student.std_id=login.std_id JOIN instructor ON student.std_instructor=instructor.instructor_id WHERE login.id='%s'"%user
    )
    result=cur.fetchall()
    return render_template('mypage.html', user=result[0])


@app.route('/changepw', methods=['GET', 'POST'])
def changepw():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['pw']
        cur.execute(
            "UPDATE login SET pw='%s' WHERE id = '%s';" % (hashlib.sha512(password.encode()).hexdigest(), id)
        )
        cur.commit()
        flash('Updated')
        return render_template('login.html')
    return render_template('changepw.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        cur.execute(
            "SELECT * FROM login WHERE id='%s' AND pw='%s';" % (id, hashlib.sha512(password.encode()).hexdigest()))
        result = cur.fetchall()
        user=result[0]['id']
        if len(result) != 1:
            flash('No Matching Information')
            return render_template('login.html')
        elif id == 'admin':
            return render_template('admin.html', user=user)
        else:
            return render_template('mainpage.html', user=user)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    std_id = request.form['std_id']
    id = request.form['id']
    password = request.form['password']
    cur.execute("SELECT std_id FROM login WHERE std_id='%s'"%std_id)
    result=cur.fetchall()
    if len(result)==1:
        cur.execute(
            "INSERT INTO login VALUES ('%s', '%s', '%s');" % (std_id, id, hashlib.sha512(password.encode()).hexdigest())
        )
        cur.commit()
        flash('Registered')
        return render_template('login.html')
    flash('No Corresponding Student ID Entry')
    return render_template('register.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # TODO
    # 기본 검색 기능은 일반 유저와 동일하게 가능하도록.
    if request.method == 'POST':
        if request.form.get('submit2') == "submit2":
            # TODO
            # 과목 추가 기능
            print(request.form)
            course_id = request.form['course_id']
            section_id = request.form['section_id']
            course_name = request.form['course_name']
            dept_name = request.form['dept_name']
            type = request.form['type']
            credits = request.form['credits']
            hour = request.form['hour']
            year = request.form['year']
            semester = request.form['semester']
            instructor_id = request.form['instructor_id']
            cur.execute(
                "INSERT INTO course VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (
                    course_id, course_name, dept_name, type, credits, hour)
            )
            cur.execute(
                "INSERT INTO section VALUES (%s,'%s','%s','%s','%s','%s');" % (
                    "DEFAULT", course_id, section_id, year, semester, instructor_id)
            )
            flash('Added')
            return render_template('admin.html')
        elif request.form.get('delete') == "delete":
            # 과목 삭제 기능
            dcourse_id = request.form['dcourse_id']
            dyear = request.form['dyear']
            dsemester = request.form['dsemester']
            dsection_id = request.form['dsection_id']
            cur.execute(
                "DELETE FROM section WHERE (course_id, section_id, year, semester) = ('%s','%s', '%s','%s')" %(dcourse_id, dsection_id, dyear, dsemester)
            )
            flash('Deleted')
            return render_template('admin.html')
        else:
            query = 'SELECT * FROM (section JOIN instructor ON section.instructor_id=instructor.instructor_id) AS temp1, (course JOIN department ON course.dept_name=department.dept_name) AS temp2 WHERE temp2.course_id=temp1.course_id'
            if request.form.get('submit') == "submit":
                year = request.form['pYear']
                semester = request.form['pTerm']
                college = request.form['pCol']
                credit = request.form['pCredit']
                instructor = request.form['pProf']
                course_id = request.form['pCourCd']
                section_id = request.form['pCourCls']
                course_name = request.form['pCourNm']
                # TODO
                if year != '':
                    query += " AND temp1.year=%d" % int(year)
                if semester != '':
                    query += " AND temp1.semester='%s'" % semester
                if college != '':
                    if college=='교양':
                        query+=" AND temp2.type='elective'"
                    else:
                        query+=" AND temp2.type<>'elective' AND temp2.college_name='%s'"%college
                if credit != '':
                    query+=" AND temp2.credits=%d"%int(credit)
                if instructor != '':
                    query+=" AND temp1.instructor_name LIKE '%%%s%%'"%instructor
                if course_id != '':
                    query+=" AND temp2.course_id LIKE '%%%s%%'"%course_id
                if section_id != '':
                    query+=" AND temp1.section_id LIKE '%%%s%%'"%section_id
                if course_name != '':
                    query+=" AND temp2.course_name LIKE '%%%s%%'"%course_name
            query+=' ORDER BY temp1.course_id, temp1.section_id ASC;'
            cur.execute(query)
            result = cur.fetchall()
            modified=[]
            for i in range(len(result)):
                query2="SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s' ORDER BY timeslot_id ASC;"%result[i]['id']
                cur.execute(query2)
                temp=cur.fetchall()
                result[i]['timeslot']=[]
                for j in temp:
                    result[i]['timeslot'].append((j['day']+' ' if j['day'] is not None else '')+(str(j['period'])+'교시 ' if j['period'] is not None else '')+(j['building']+' ' if j['building'] is not None else '')+(j['building_address']+' ' if j['building_address'] is not None else '')+(j['place_name'] if j['place_name'] is not None else ''))
            for i in result:
                query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s'" % i['id']
                day = request.form['pDay']
                time = request.form['pStartTime']
                if day!='':
                    query2+=" AND day='%s'"%day
                if time!='':
                    query2+=" AND period=%d"%int(time)
                query2+=' ORDER BY timeslot_id ASC;'
                cur.execute(query2)
                temp=cur.fetchall()
                if request.method != 'POST' or request.method == 'POST' and (day!='' or time!='') and len(temp)>0 or request.method == 'POST' and day=='' and time=='':
                    modified.append(i)
            return render_template('admin.html', courses=modified)
    query = 'SELECT * FROM (section JOIN instructor ON section.instructor_id=instructor.instructor_id) AS temp1, (course JOIN department ON course.dept_name=department.dept_name) AS temp2 WHERE temp2.course_id=temp1.course_id'
    query+=' ORDER BY temp1.course_id, temp1.section_id ASC;'
    cur.execute(query)
    result = cur.fetchall()
    modified=[]
    for i in range(len(result)):
        query2="SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s' ORDER BY timeslot_id ASC;"%result[i]['id']
        cur.execute(query2)
        temp=cur.fetchall()
        result[i]['timeslot']=[]
        for j in temp:
            result[i]['timeslot'].append((j['day']+' ' if j['day'] is not None else '')+(str(j['period'])+'교시 ' if j['period'] is not None else '')+(j['building']+' ' if j['building'] is not None else '')+(j['building_address']+' ' if j['building_address'] is not None else '')+(j['place_name'] if j['place_name'] is not None else ''))
    for i in result:
        query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s'" % i['id']
        query2+=' ORDER BY timeslot_id ASC;'
        cur.execute(query2)
        temp=cur.fetchall()
        if request.method != 'POST' or request.method == 'POST' and (day!='' or time!='') and len(temp)>0 or request.method == 'POST' and day=='' and time=='':
            modified.append(i)
    return render_template('admin.html', courses=modified)


if __name__ == '__main__':
    app.run()