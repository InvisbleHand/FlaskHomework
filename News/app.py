from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/news_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = '1A45fG-39kLpZ_7bHjM_6QxY-2cDvP_9eSjT-8uAwE'

db = SQLAlchemy(app)

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    news_list = News.query.order_by(News.created_date.desc()).all()
    return render_template("lists.html", news_list=news_list)


@app.route("/article/<int:news_id>", methods=["GET"])
def article(news_id):
    news_item = News.query.get_or_404(news_id)
    return render_template("article.html", news=news_item)


@app.route("/create", methods=["GET", "POST"])
def create_news():
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")

        if not title.strip() or not content.strip():
            return "标题或者内容不为空", 400
        
        new_item = News(
            title=title.strip(), 
            content=content.strip(), 
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
    app.run(debug=False)