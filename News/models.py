from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(255), nullable=True) 
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'), nullable=False)

class Category(db.Model):
    __tablename__  = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False) 
    news = db.relationship('News', backref='category', lazy='dynamic')   