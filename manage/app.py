from flask import Flask, redirect, session, render_template, url_for
from models import db 
from routes.auth import auth_bp 
from routes.manage import manage_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/manage_stu_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '63f68a735e5d17c918b84b5c7e0c4a4512e02d87e0743b14'     
    
    db.init_app(app)

    app.register_blueprint(auth_bp) 
    app.register_blueprint(manage_bp)

    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('manage.html')
    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all() 

    app.run(debug=False)