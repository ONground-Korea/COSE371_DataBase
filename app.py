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
connect.autocommit = True
cur = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
user = None


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/main')
def main():
    global user
    return render_template('mainpage.html', user=user)


@app.route('/mycourses')
def mycourses():
    global user
    query = "SELECT s.id AS idx, s.course_id, s.section_id, s.year, s.semester, s.instructor_name, s.college_name, s.dept_name, c.*, temp.* \
            FROM (section JOIN instructor ON section.instructor_id=instructor.instructor_id) AS s, \
            (course JOIN department ON course.dept_name=department.dept_name) AS c, \
            (takes JOIN login ON takes.std_id=login.std_id) AS temp \
            WHERE c.course_id=s.course_id AND s.id=temp.section_id AND temp.id='%s' \
            ORDER BY s.year, s.semester, s.course_id, s.section_id ASC;" % user
    cur.execute(query)
    result = cur.fetchall()
    for i in range(len(result)):
        query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp \
                LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s' ORDER BY timeslot_id ASC;" % result[i][
            'idx']
        cur.execute(query2)
        temp = cur.fetchall()
        result[i]['timeslot'] = []
        for j in temp:
            result[i]['timeslot'].append((j['day'] + ' ' if j['day'] is not None else '') + (
                str(j['period']) + '교시 ' if j['period'] is not None else '') + (
                                             j['building'] + ' ' if j['building'] is not None else '') + (
                                             j['building_address'] + ' ' if j[
                                                                                'building_address'] is not None else '') + (
                                             j['place_name'] if j['place_name'] is not None else ''))
        query3 = "SELECT prereq_id FROM prereq WHERE course_id='%s' ORDER BY prereq_id ASC;" % result[i]['course_id']
        cur.execute(query3)
        temp2 = cur.fetchall()
        result[i]['prereq'] = []
        for j in temp2:
            result[i]['prereq'].append(j['prereq_id'])
    return render_template('mycourses.html', courses=result)


@app.route('/allcourses', methods=['GET', 'POST'])
def allcourses():
    query = 'SELECT * FROM (section JOIN instructor ON section.instructor_id=instructor.instructor_id) AS temp1, \
            (course JOIN department ON course.dept_name=department.dept_name) AS temp2 WHERE temp2.course_id=temp1.course_id'
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

            if year != '':
                query += " AND temp1.year=%d" % int(year)
            if semester != '':
                query += " AND temp1.semester='%s'" % semester
            if college != '':
                if college == '교양':
                    query += " AND temp2.type='elective'"
                else:
                    query += " AND temp2.type<>'elective' AND temp2.college_name='%s'" % college
            if credit != '':
                query += " AND temp2.credits=%d" % int(credit)
            if instructor != '':
                query += " AND temp1.instructor_name LIKE '%%%s%%'" % instructor
            if course_id != '':
                query += " AND temp2.course_id LIKE '%%%s%%'" % course_id
            if section_id != '':
                query += " AND temp1.section_id LIKE '%%%s%%'" % section_id
            if course_name != '':
                query += " AND temp2.course_name LIKE '%%%s%%'" % course_name
    query += ' ORDER BY temp1.year, temp1.semester, temp1.course_id, temp1.section_id ASC;'
    cur.execute(query)
    result = cur.fetchall()
    modified = []
    for i in range(len(result)):
        query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp \
                LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s' ORDER BY timeslot_id ASC;" % result[i][
            'id']
        cur.execute(query2)
        temp = cur.fetchall()
        result[i]['timeslot'] = []
        for j in temp:
            result[i]['timeslot'].append((j['day'] + ' ' if j['day'] is not None else '') + (
                str(j['period']) + '교시 ' if j['period'] is not None else '') + (
                                             j['building'] + ' ' if j['building'] is not None else '') + (
                                             j['building_address'] + ' ' if j[
                                                                                'building_address'] is not None else '') + (
                                             j['place_name'] if j['place_name'] is not None else ''))
        query3 = "SELECT prereq_id FROM prereq WHERE course_id='%s' ORDER BY prereq_id ASC;" % result[i]['course_id']
        cur.execute(query3)
        temp2 = cur.fetchall()
        result[i]['prereq'] = []
        for j in temp2:
            result[i]['prereq'].append(j['prereq_id'])
    for i in result:
        query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp \
                LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s'" % i['id']
        if request.method == 'POST':
            day = request.form['pDay']
            time = request.form['pStartTime']
            if day != '':
                query2 += " AND day='%s'" % day
            if time != '':
                query2 += " AND period=%d" % int(time)
        query2 += ' ORDER BY timeslot_id ASC;'
        cur.execute(query2)
        temp = cur.fetchall()
        if request.method != 'POST' or request.method == 'POST' and (day != '' or time != '') and len(
                temp) > 0 or request.method == 'POST' and day == '' and time == '':
            modified.append(i)
    return render_template('allcourses.html', courses=modified)


@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    global user
    if request.method == 'POST':
        std_id = request.form['std_id']
        cur.execute(
            "DELETE FROM login WHERE std_id = '%s' AND id='%s';" % (std_id, user)
        )
        flash('Eliminated')
        user = None
        return render_template('login.html')
    cur.execute(
        "SELECT * FROM student JOIN login ON student.std_id=login.std_id JOIN instructor ON student.std_instructor=instructor.instructor_id WHERE login.id='%s'" % user
    )
    result = cur.fetchall()
    cur.execute(
        "SELECT (SUM(credits*number)/SUM(credits))::NUMERIC(3,2) \
        FROM (takes LEFT JOIN section ON takes.section_id=section.id) AS temp \
        LEFT JOIN course ON course.course_id=temp.course_id LEFT JOIN grades ON temp.grade=grades.alphabet \
        JOIN login ON temp.std_id=login.std_id WHERE login.id='%s' AND temp.grade IS NOT NULL;" % user
    )
    gpa = cur.fetchall()
    return render_template('mypage.html', user=result[0], gpa=gpa[0]['numeric'])


@app.route('/changepw', methods=['GET', 'POST'])
def changepw():
    global user
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['pw']
        confirm_password = request.form['comfirm_pw']
        if id != user:
            flash('Access Denied')
            return render_template('changepw.html')
        if password != confirm_password:
            flash('Password Comfirmation Failed')
            return render_template('changepw.html')
        cur.execute(
            "UPDATE login SET pw='%s' WHERE id = '%s';" % (hashlib.sha512(password.encode()).hexdigest(), id)
        )
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
        if len(result) != 1:
            flash('No Matching Information')
            return render_template('login.html')
        elif id == 'admin':
            user = result[0]['id']
            return redirect(url_for('admin'))
            # return render_template('admin.html', user=user)
        else:
            user = result[0]['id']
            return render_template('mainpage.html', user=user)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        std_id = request.form['std_id']
        id = request.form['id']
        password = request.form['password']
        cur.execute("SELECT COUNT(std_id) FROM student WHERE std_id='%s'" % std_id)
        result = cur.fetchall()
        cur.execute("SELECT COUNT(id) FROM login WHERE std_id='%s' OR id='%s'" % (std_id, id))
        result2 = cur.fetchall()
        if result[0]['count'] == 1 and result2[0]['count'] == 0:
            cur.execute(
                "INSERT INTO login VALUES ('%s', '%s', '%s');" % (
                std_id, id, hashlib.sha512(password.encode()).hexdigest())
            )
            flash('Registered')
            return render_template('login.html')
        print(result[0])
        flash('No Corresponding Student ID Entry' if result[0]['count'] == 0 else 'Already Exists')
        return render_template('register.html')
    return render_template('register.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('submit2') == "submit2":
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
            day = request.form['day']
            time = request.form['time']
            prereq_id = request.form['prereq_id']
            building = request.form['building']
            building_address = request.form['building_address']
            cur.execute("SELECT COUNT(course_id) FROM course WHERE course_id='%s'" % course_id)
            result = cur.fetchall()
            if result[0]['count'] == 0:
                cur.execute(
                    "INSERT INTO course VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (
                        course_id, course_name, dept_name, type, credits, hour)
                )
            if prereq_id != '':
                cur.execute("SELECT COUNT(course_id) FROM course WHERE course_id='%s'" % prereq_id)
                result = cur.fetchall()
                if result[0]['count'] == 1:
                    cur.execute("SELECT COUNT(course_id) FROM prereq WHERE course_id='%s' AND prereq_id='%s'" % (
                    course_id, prereq_id))
                    result = cur.fetchall()
                    if result[0]['count'] == 0:
                        cur.execute("INSERT INTO prereq VALUES ('%s', '%s')" % (course_id, prereq_id))
                    else:
                        flash("Prerequisite Already Exists")
                        return render_template('admin.html')
                else:
                    flash("Course ID Corresponding to Prerequisite ID Does Not Exist")
                    return render_template('admin.html')
            cur.execute("SELECT COUNT(id) FROM section \
                        WHERE year=%d AND semester='%s' AND course_id='%s' AND section_id='%s'" \
                        % (int(year), semester, course_id, section_id))
            result = cur.fetchall()
            if result[0]['count'] == 0:
                cur.execute(
                    "INSERT INTO section VALUES (DEFAULT,'%s','%s','%d','%s','%s');" \
                    % (course_id, section_id, int(year), semester, instructor_id)
                )
            cur.execute("SELECT COUNT(section_time.section_id) FROM section_time JOIN section ON section_time.section_id=section.id \
                        JOIN timeslot ON section_time.timeslot_id=timeslot.id \
                        WHERE year=%d AND semester='%s' AND course_id='%s' AND section.section_id='%s' AND day='%s' AND period=%d" \
                        % (int(year), semester, course_id, section_id, day, int(time)))
            result = cur.fetchall()
            if result[0]['count'] == 0:
                cur.execute("INSERT INTO section_time \
                            VALUES ((SELECT id FROM section WHERE year=%d AND semester='%s' AND course_id='%s' AND section_id='%s'), \
                            (SELECT id FROM timeslot WHERE day='%s' AND period=%d), \
                            (SELECT id FROM place WHERE building='%s' AND building_address='%s'))" \
                            % (int(year), semester, course_id, section_id, day, int(time), building, building_address))
            else:
                flash('Already Exists')
                return render_template('admin.html')
            flash('Added')
            return render_template('admin.html')
        elif request.form.get('delete') == "delete":
            dcourse_id = request.form['dcourse_id']
            dyear = request.form['dyear']
            dsemester = request.form['dsemester']
            dsection_id = request.form['dsection_id']
            cur.execute(
                "SELECT * FROM section WHERE (course_id, section_id, year, semester)=('%s', '%s', '%s', '%s')" % (
                dcourse_id, dsection_id, dyear, dsemester))
            result = cur.fetchall()
            if len(result) > 0:
                cur.execute(
                    "DELETE FROM section WHERE (course_id, section_id, year, semester) = ('%s','%s', '%s','%s')" % (
                    dcourse_id, dsection_id, dyear, dsemester)
                )
                flash('Deleted')
            else:
                flash("Section Does Not Exist")
            return render_template('admin.html')
        else:
            query = 'SELECT * FROM (section JOIN instructor ON section.instructor_id=instructor.instructor_id) AS temp1, \
                    (course JOIN department ON course.dept_name=department.dept_name) AS temp2 WHERE temp2.course_id=temp1.course_id'
            if request.form.get('submit') == "submit":
                year = request.form['pYear']
                semester = request.form['pTerm']
                college = request.form['pCol']
                credit = request.form['pCredit']
                instructor = request.form['pProf']
                course_id = request.form['pCourCd']
                section_id = request.form['pCourCls']
                course_name = request.form['pCourNm']
                if year != '':
                    query += " AND temp1.year=%d" % int(year)
                if semester != '':
                    query += " AND temp1.semester='%s'" % semester
                if college != '':
                    if college == '교양':
                        query += " AND temp2.type='elective'"
                    else:
                        query += " AND temp2.type<>'elective' AND temp2.college_name='%s'" % college
                if credit != '':
                    query += " AND temp2.credits=%d" % int(credit)
                if instructor != '':
                    query += " AND temp1.instructor_name LIKE '%%%s%%'" % instructor
                if course_id != '':
                    query += " AND temp2.course_id LIKE '%%%s%%'" % course_id
                if section_id != '':
                    query += " AND temp1.section_id LIKE '%%%s%%'" % section_id
                if course_name != '':
                    query += " AND temp2.course_name LIKE '%%%s%%'" % course_name
            query += ' ORDER BY temp1.course_id, temp1.section_id ASC;'
            cur.execute(query)
            result = cur.fetchall()
            modified = []
            for i in range(len(result)):
                query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp \
                        LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s' ORDER BY timeslot_id ASC;" % \
                         result[i]['id']
                cur.execute(query2)
                temp = cur.fetchall()
                result[i]['timeslot'] = []
                for j in temp:
                    result[i]['timeslot'].append((j['day'] + ' ' if j['day'] is not None else '') + (
                        str(j['period']) + '교시 ' if j['period'] is not None else '') + (
                                                     j['building'] + ' ' if j['building'] is not None else '') + (
                                                     j['building_address'] + ' ' if j[
                                                                                        'building_address'] is not None else '') + (
                                                     j['place_name'] if j['place_name'] is not None else ''))
                query3 = "SELECT prereq_id FROM prereq WHERE course_id='%s' ORDER BY prereq_id ASC;" % result[i][
                    'course_id']
                cur.execute(query3)
                temp2 = cur.fetchall()
                result[i]['prereq'] = []
                for j in temp2:
                    result[i]['prereq'].append(j['prereq_id'])
            for i in result:
                query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp \
                        LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s'" % i['id']
                day = request.form['pDay']
                time = request.form['pStartTime']
                if day != '':
                    query2 += " AND day='%s'" % day
                if time != '':
                    query2 += " AND period=%d" % int(time)
                query2 += ' ORDER BY timeslot_id ASC;'
                cur.execute(query2)
                temp = cur.fetchall()
                if (day != '' or time != '') and len(temp) > 0 or day == '' and time == '':
                    modified.append(i)
            return render_template('admin.html', courses=modified)
    query = 'SELECT * FROM (section JOIN instructor ON section.instructor_id=instructor.instructor_id) AS temp1, \
            (course JOIN department ON course.dept_name=department.dept_name) AS temp2 WHERE temp2.course_id=temp1.course_id'
    query += ' ORDER BY temp1.course_id, temp1.section_id ASC;'
    cur.execute(query)
    result = cur.fetchall()
    for i in range(len(result)):
        query2 = "SELECT * FROM (section_time LEFT JOIN timeslot ON section_time.timeslot_id=timeslot.id) AS temp \
                LEFT JOIN place ON temp.place_id=place.id WHERE section_id='%s' ORDER BY timeslot_id ASC;" % result[i][
            'id']
        cur.execute(query2)
        temp = cur.fetchall()
        result[i]['timeslot'] = []
        for j in temp:
            result[i]['timeslot'].append((j['day'] + ' ' if j['day'] is not None else '') + (
                str(j['period']) + '교시 ' if j['period'] is not None else '') + (
                                             j['building'] + ' ' if j['building'] is not None else '') + (
                                             j['building_address'] + ' ' if j[
                                                                                'building_address'] is not None else '') + (
                                             j['place_name'] if j['place_name'] is not None else ''))
        query3 = "SELECT prereq_id FROM prereq WHERE course_id='%s' ORDER BY prereq_id ASC;" % result[i]['course_id']
        cur.execute(query3)
        temp2 = cur.fetchall()
        result[i]['prereq'] = []
        for j in temp2:
            result[i]['prereq'].append(j['prereq_id'])
    return render_template('admin.html', courses=result)


if __name__ == '__main__':
    app.run()