from functools import wraps

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from .models import (
    create_user,
    delete_user,
    fetch_users,
    get_monthly_attendance_summary,
    get_user_by_id,
    update_user,
)

admin = Blueprint('admin', __name__)


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin dashboard.', 'warning')
            return redirect(url_for('admin.login'))
        return view(*args, **kwargs)

    return wrapped_view


@admin.route('', methods=['GET'])
@admin.route('/', methods=['GET'])
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''

        if username == current_app.config.get('ADMIN_USERNAME') and password == current_app.config.get('ADMIN_PASSWORD'):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))

        flash('Invalid admin username or password.', 'danger')

    return render_template('admin_login.php')


@admin.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out.', 'success')
    return redirect(url_for('admin.login'))


@admin.route('/dashboard', methods=['GET', 'POST'])
@admin_required
def dashboard():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        rfid_tag = (request.form.get('rfid_tag') or '').strip()
        if not name or not rfid_tag:
            flash('Name and RFID tag are required.', 'warning')
        else:
            create_user(name, rfid_tag)
            flash('User was registered successfully.', 'success')

    users = fetch_users()
    report = get_monthly_attendance_summary()
    return render_template(
        'admin_dashboard.php',
        users=users,
        report=report,
        total_users=len(users),
        total_records=sum(item['total'] for item in report),
    )


@admin.route('/users/<int:user_id>/edit', methods=['POST'])
@admin_required
def update_user_route(user_id):
    name = (request.form.get('name') or '').strip()
    rfid_tag = (request.form.get('rfid_tag') or '').strip()

    if not name or not rfid_tag:
        flash('Name and RFID tag are required to update the user.', 'warning')
        return redirect(url_for('admin.dashboard'))

    user = get_user_by_id(user_id)
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.dashboard'))

    update_user(user_id, name, rfid_tag)
    flash('User updated successfully.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user_route(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        flash('User was not found.', 'danger')
    else:
        delete_user(user_id)
        flash(f'{user["name"]} was removed successfully.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin.route('/report')
@admin_required
def report():
    report_data = get_monthly_attendance_summary()
    return render_template('admin_report.php', report=report_data)
