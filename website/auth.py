from flask import Blueprint, flash, redirect, render_template, request, url_for

from .models import (
    create_user,
    fetch_users,
    get_recent_attendance,
    get_user_by_rfid,
    has_attendance_today,
    normalize_rfid,
    register_attendance,
)

auth = Blueprint('auth', __name__)


@auth.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        rfid_number = normalize_rfid(request.form.get('rfid_number'))
        if not rfid_number:
            flash('Please tap or enter a valid RFID tag.', 'warning')
            return redirect(url_for('auth.attendance'))

        user = get_user_by_rfid(rfid_number)
        if user is None:
            flash('RFID tag is not registered. Please contact the admin.', 'danger')
            return redirect(url_for('auth.attendance'))

        if has_attendance_today(user['id']):
            flash(f'{user["name"]} has already recorded attendance today.', 'info')
            return redirect(url_for('auth.attendance'))

        register_attendance(user['id'], rfid_number)
        flash(f'Attendance recorded for {user["name"]}.', 'success')
        return redirect(url_for('auth.attendance'))

    recent = get_recent_attendance(limit=10)
    users = fetch_users()
    return render_template('attendance.php', users=users, recent_attendance=recent)


@auth.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        rfid_tag = (request.form.get('rfid_tag') or '').strip()

        if not name or not rfid_tag:
            flash('Name and RFID Tag are required.', 'warning')
            return redirect(url_for('auth.add_user'))

        try:
            create_user(name, rfid_tag)
            flash('User registered successfully.', 'success')
        except Exception:
            flash('This RFID tag is already registered. Use a different one.', 'danger')
        return redirect(url_for('auth.add_user'))

    return render_template('add_user.php')


@auth.route('/user-list', methods=['GET'])
def user_list():
    users = fetch_users()
    return render_template('user_list.php', users=users)