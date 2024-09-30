
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
db = SQLAlchemy(app)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    time_in = db.Column(db.Time, nullable=False)

@app.route('/attendance_list/<int:year>/<int:month>')
def attendance_list(year, month):
    # Get the first and last day of the month
    month_start = datetime(year, month, 1)
    if month == 12:
        month_end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = datetime(year, month + 1, 1) - timedelta(days=1)

    # Query attendance records for the specific month
    attendance_list = Attendance.query.filter(
        Attendance.date >= month_start,
        Attendance.date <= month_end
    ).all()
    
    return render_template('attendance_list.html', 
                           attendance_list=attendance_list,
                           month_start=month_start,
                           month_end=month_end)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'animax'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

