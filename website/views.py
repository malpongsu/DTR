from flask import Blueprint, redirect, render_template, url_for

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return redirect(url_for('auth.attendance'))


@views.route('/home')
def home_page():
    return render_template('home.php')