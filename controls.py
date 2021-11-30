import os
# from app import app
import urllib.request
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from dbase import mydbase, mycursor
import string, random


size = 3000
randomlink = ''.join(random.choices(string.ascii_letters+string.digits, k=size))
randomStrings = str(randomlink)

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    rnd=randomStrings
    return render_template('index.html')

@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    # Admin Login
    message = ''
    username = 'Master'
    password = 'Machine'
    if request.method == 'GET':
        return render_template('adminLogin.html')
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        if _username == username and _password == password:
            message = 'Done'
            return redirect(f'/admin/{randomStrings}')
        else:
            message = 'Wrong Admin Password Try Again'
            return render_template('index.html', message = message)

@app.route('/studentLogin', methods=['GET', 'POST'])
def studentLogin():
    # Student Login
    message = ''
    if request.method == 'GET':
        return render_template('studentLogin.html')
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        mycursor.execute(f'SELECT * FROM student WHERE name = "{_username}" AND stu_id = "{_password}" ')
        check = mycursor.fetchone()
        if check:
            mycursor.execute(f"SELECT * FROM student WHERE ID={check['ID']}")
            students = mycursor.fetchone()
            return render_template('profile.html', students = students)
        else:
            message = 'Wrong Student Password Try Again'
            return render_template('index.html', message = message)

@app.route(f'/admin/{randomStrings}')
def admin():
    return render_template('admin.html')

@app.route('/list', methods = ['GET', 'POST'])
def List():
    mycursor.execute("SELECT * FROM student")
    student = mycursor.fetchall()
    return render_template('list.html', student = student)

@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        _name = request.form['name']
        _stu_id = request.form['stu_id']
        _age = request.form['age']
        _mobile = request.form['mobile']
        sql = 'INSERT INTO student (name, stu_id, age, mobile) VALUES (%s, %s, %s, %s)'
        val = (_name, _stu_id, _age, _mobile)
        mycursor.execute(sql, val)
        mydbase.commit()
        return redirect('/list')

@app.route('/list', methods=['GET', 'POST'])
def view():
    if request.method == 'GET':
        return render_template('list.html')

@app.route('/details/<int:id>')
def students_details(id):
    mycursor.execute(f'SELECT * FROM student WHERE ID={id}')
    students = mycursor.fetchone()

    mycursor.execute(f'SELECT * FROM fee WHERE student_id={id}')
    payments = mycursor.fetchall()

    mycursor.execute(f'SELECT * FROM course WHERE course_id={id}')
    courses = mycursor.fetchall()

    mycursor.execute(f'SELECT * FROM exams WHERE exam_id={id}')
    exams = mycursor.fetchall()

    return render_template('student_detail.html', students = students, payments = payments, courses = courses, exams = exams
    )

# @app.route('/edit/<int:id>', methods=['GET', 'POST'])
# def edit_customer(id):
#     if request.method == 'GET':
#         mycursor.execute(f'SELECT * FROM student WHERE ID={id}')
#         student = mycursor.fetchone()
#         return render_template('edit_student.html', student = student)
#     if request.method == 'POST':
#         _name = request.form['name']
#         _stu_id = request.form['stu_id']
#         _age = request.form['age']
#         _mobile = request.form['mobile']
#         sql = f'UPDATE student SET name = %s, stu_id = %s, age = %s , mobile = %s WHERE ID = %s'
#         values = (_name, _stu_id, _age, _mobile, id)
#         mycursor.execute(sql, values)
#         mydbase.commit()
#         return redirect('/register')


@app.route('/delete/<int:id>')
def delete_students(id):
    sql = f'DELETE FROM student WHERE ID = {id}'
    mycursor.execute(sql)
    mydbase.commit()
    return redirect('/list')

@app.route('/fee/<int:id>', methods=['GET', 'POST'])
def update_fee(id):
    if request.method == 'GET':
        return render_template('fee_form.html', id = id)
    if request.method == 'POST':
        amount = request.form['amount']
        payment_type = request.form['type']
        sql = "INSERT INTO fee (amount, type, student_id) VALUES (%s, %s, %s)"
        values = (amount, payment_type, id)
        mycursor.execute(sql, values)
        mydbase.commit()
        return redirect(f'/details/{id}')

@app.route('/course/<int:id>', methods=['GET', 'POST'])
def update_course(id):
    if request.method == 'GET':
        return render_template('course_form.html', id = id)
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_type = request.form['course_type']
        sql = "INSERT INTO course(course_name, course_type, course_id) VALUES (%s, %s, %s)"
        value = (course_name, course_type, id)
        mycursor.execute(sql, value)
        mydbase.commit()
        return redirect(f'/details/{id}')

@app.route('/exams/<int:id>', methods=['GET', 'POST'])
def update_exam(id):
    if request.method == 'GET':
        return render_template('exam_form.html', id = id)
    if request.method == 'POST':
        exam_code = request.form['exam_code']
        exam_type = request.form['exam_type']
        exam_score = request.form['exam_score']
        sql = "INSERT INTO exams(exam_code, exam_type, exam_score, exam_id) VALUES (%s, %s, %s, %s)"
        value = (exam_code, exam_type, exam_score, id)
        mycursor.execute(sql, value)
        mydbase.commit()
        return redirect(f'/details/{id}')

if __name__ == '__main__':
    app.run(debug=True)