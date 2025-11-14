import os
from flask import Flask, redirect, render_template, request, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from uuid import uuid4
from datetime import datetime

from config import Config   
from models import db, News
from utils import allowed_file


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app

app = create_app()


@app.route("/", methods=["GET"])
def home():
    news_list = News.query.order_by(News.created_date.desc()).all()
    return render_template("home.html", news_list=news_list)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     return render_template("login.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     hashed_password = generate_password_hash(password, method='scrypt')

#     user_exists = User.query.filter_by(username=username).first()
#     if user_exists:
#         flash("用户名已存在！", "error")
#         return redirect(url_for('register'))

#     new_user = User(username=username, password_hash=hashed_password)

#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     except Exception as e:
#         db.session.rollback()
#         flash(f"注册失败: {e}", "error")
#         return redirect(url_for('register'))


@app.route("/article/<int:news_id>", methods=["GET"])
def article(news_id):
    news_item = News.query.get_or_404(news_id)
    return render_template("article.html", news=news_item)


@app.route("/create", methods=["GET", "POST"])
def create_news():
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        cover_image_path = None

        file = request.files.get('cover_image')
        if file and file.filename and allowed_file(file.filename, app.config):
            upload_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = f"{uuid4().hex}_{secure_filename(file.filename)}"
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            cover_image_path = f"imgs/{filename}"

        if not title.strip() or not content:
            flash('标题和内容不能为空！', 'error')
            return redirect(url_for('create_news'))
        
        new_item = News(
            title=title.strip(), 
            content=content,
            cover_image=cover_image_path,
            created_date=datetime.now()
        )
        try:
            db.session.add(new_item)
            db.session.commit()
            
            flash('文章发表成功！', 'success') 
            return redirect(url_for('home'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'文章发表失败: {e}', 'error')
            return redirect(url_for('create_news'))
        
    return render_template("create_news.html")


if __name__ == "__main__":
    app.run(debug=True)