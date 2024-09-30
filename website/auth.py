from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/attendance', methods=['GET', 'POST'])
def attendance():
    return render_template("attendance.php", boolean=True)

@auth.route('/add-user')
def logout():
    return render_template("add_user.php", boolean=True)

@auth.route('/user-list', methods=['GET', 'POST'])
def sign_up():
    return render_template("user_list.php")