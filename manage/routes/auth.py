from flask import Blueprint, request, redirect, render_template, session, url_for 
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Teacher 
from utils import alert_error

auth_bp = Blueprint('auth', __name__) 

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return alert_error("用户名或密码不能为空")

        teacher = Teacher.query.filter_by(name=username).first()
            
        if teacher and check_password_hash(teacher.password_hash, password):             
            session['user_id'] = teacher.id
            session['username'] = teacher.name
            return redirect('/') 
        else:
            return alert_error("用户名或密码错误，请重试")

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        rePassword = request.form.get('rePassword')

        if not username or not password:
            return alert_error("用户名或密码不能为空")
        
        if rePassword != password:
            return alert_error("两次密码不一致")

        if Teacher.query.filter_by(name=username).first():
            return alert_error("该用户名已被注册")

        password_hash = generate_password_hash(password)

        new_teacher = Teacher(name=username, password_hash=password_hash)
        db.session.add(new_teacher)
        db.session.commit()
        return redirect(url_for('auth.login')) 

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))