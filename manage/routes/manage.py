from flask import Blueprint, request, redirect, render_template, url_for
from models import db, Student 
from utils import alert_error 

manage_bp = Blueprint('manage', __name__) 

@manage_bp.route('/', methods=['GET']) 
def index():
    students = db.session.query(Student).all() 
    return render_template('manage.html', students=students)


@manage_bp.route('/add', methods=['POST']) 
def add():
    student_name = request.form.get('studentName') 
    grade_str = request.form.get('studentScore')

    validate_input(student_name, grade_str)
    
    new_student = Student(name=student_name, grade=int(grade_str))
    db.session.add(new_student)
    db.session.commit()
    
    return redirect(url_for('manage.index'))


@manage_bp.route('/delete/<int:student_id>', methods=['GET'])
def delete(student_id):
    student = db.get_or_404(Student, student_id) 
    db.session.delete(student) 
    db.session.commit() 
    return redirect(url_for('manage.index'))


@manage_bp.route('/edit', methods=['POST'])
def edit():
    student_id = request.form.get('studentId')
    student = db.get_or_404(Student, student_id) 

    new_name = request.form.get('studentName') 
    new_grade_str = request.form.get('studentScore')

    validate_input(new_name, new_grade_str)

    student.name = new_name
    student.grade = int(new_grade_str)
    db.session.commit() 

    return redirect(url_for('manage.index'))
    
    
def validate_input(name, grade_str):
    if not name or not grade_str:
        return alert_error("学生姓名或成绩不能为空")

    if len(name) > 10 or len(grade_str) > 10:
        return alert_error("长度不能超过10个字符")

    try:
        int(grade_str)
    except ValueError:
        return alert_error("成绩输入必须是有效的整数")
    
    return None