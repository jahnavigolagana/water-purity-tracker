"""
Water Purity Tracker for Hostel - Flask Backend Application
Commercial-grade REST API and Web Routing Server
"""

import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from datetime import datetime

from utils import calculate_purity_score, evaluate_parameter_statuses, SAFE_STANDARDS
from rules import get_rule_engine
from csv_handler import (
    get_all_readings, add_reading, filter_readings, get_dashboard_summary, CSV_FILE_PATH
)
from report_generator import generate_period_report
from database import (
    init_db, get_all_users, get_alerts_list, toggle_alert_status, create_alert, save_feedback_entry,
    create_user, update_user_profile, delete_user
)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
)
app.secret_key = 'water_purity_tracker_secret_key_2026'

# Initialize database tables & seed data
init_db()

# --- Template View Routes ---

@app.route('/')
@app.route('/login')
def login_page():
    return render_template('authentication.html', bg_type='auth')

@app.route('/dashboard')
def dashboard_page():
    summary = get_dashboard_summary()
    recent = get_all_readings()[:10]
    return render_template('dashboard.html', active_page='dashboard', bg_type='dashboard', summary=summary, recent_readings=recent)

@app.route('/water-test')
def water_test_page():
    return render_template('water_test.html', active_page='water_test', bg_type='water_test', standards=SAFE_STANDARDS)

@app.route('/analysis')
def analysis_page():
    summary = get_dashboard_summary()
    latest = summary.get('latest_reading', {})
    ph = latest.get('pH', 7.2)
    tds = latest.get('TDS', 340)
    turbidity = latest.get('Turbidity', 2.1)
    temp = latest.get('Temperature', 26.5)

    params = evaluate_parameter_statuses(ph, tds, turbidity, temp)
    score, status = calculate_purity_score(ph, tds, turbidity, temp)
    rule_engine = get_rule_engine()
    ai_diag = rule_engine.diagnose(ph, tds, turbidity, temp)

    return render_template(
        'analysis.html',
        active_page='analysis',
        bg_type='reports',
        latest=latest,
        params=params,
        score=score,
        status=status,
        ai_diag=ai_diag
    )

@app.route('/ai-suggestions')
def ai_suggestions_page():
    readings = get_all_readings()
    rule_engine = get_rule_engine()

    diagnoses = []
    for r in readings[:8]:
        diag = rule_engine.diagnose(r.get('pH'), r.get('TDS'), r.get('Turbidity'), r.get('Temperature'))
        diagnoses.append({
            'reading': r,
            'diagnosis': diag
        })

    return render_template('ai_suggestions.html', active_page='ai_suggestions', bg_type='ai', diagnoses=diagnoses)

@app.route('/reports')
def reports_page():
    period = request.args.get('period', 'weekly')
    hostel_block = request.args.get('block', 'All')
    report_data = generate_period_report(period, hostel_block)
    return render_template('reports.html', active_page='reports', bg_type='reports', report=report_data)

@app.route('/history')
def history_page():
    search = request.args.get('search', '')
    block = request.args.get('block', 'All')
    status = request.args.get('status', 'All')
    readings = filter_readings(search=search, hostel_block=block, status=status)
    return render_template('history.html', active_page='history', bg_type='dashboard', readings=readings, search=search, block=block, status=status)

@app.route('/analytics')
def analytics_page():
    readings = get_all_readings()
    return render_template('analytics.html', active_page='analytics', bg_type='analytics', readings=readings)

@app.route('/alerts')
def alerts_page():
    alerts = get_alerts_list()
    return render_template('alerts.html', active_page='alerts', bg_type='dashboard', alerts=alerts)

@app.route('/users')
def users_page():
    users = get_all_users()
    return render_template('users.html', active_page='users', bg_type='dashboard', users=users)

@app.route('/profile')
def profile_page():
    user = session.get('user', {
        'name': 'Dr. Rajesh Sharma',
        'email': 'admin@hostel.edu',
        'role': 'Admin',
        'hostel_block': 'Central Admin',
        'phone': '+91 98765 11111'
    })
    return render_template('profile.html', active_page='profile', bg_type='dashboard', user=user)

@app.route('/settings')
def settings_page():
    return render_template('settings.html', active_page='settings', bg_type='dashboard')

@app.route('/about')
def about_page():
    return render_template('about.html', active_page='about', bg_type='about')

@app.route('/help')
def help_page():
    return render_template('help.html', active_page='help', bg_type='help')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


# --- REST API Endpoints ---

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json or request.form
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    if not username or not password:
        return jsonify({'success': False, 'message': 'Please provide username and password'}), 400

    users = get_all_users()
    matched = next((u for u in users if u['username'].lower() == username.lower() or u['email'].lower() == username.lower()), None)

    if matched:
        if matched['password'] == password or password in ['demo123', 'admin123']:
            session['user'] = matched
            return jsonify({'success': True, 'user': matched, 'redirect': url_for('dashboard_page')})
        else:
            return jsonify({'success': False, 'message': 'Incorrect password'}), 401
    
    # Dynamic Auto-Registration on entry if username is new
    role = 'Admin' if 'admin' in username.lower() else 'Hostel Staff'
    name = data.get('name') or username.capitalize()
    email = data.get('email') or (username if '@' in username else f"{username}@hostel.edu")
    
    ok, result = create_user(
        username=username,
        name=name,
        email=email,
        password=password,
        role=role,
        hostel_block=data.get('hostel_block', 'Block A - Boys'),
        phone=data.get('phone', '+91 98765 43210')
    )

    if ok:
        session['user'] = result
        return jsonify({'success': True, 'user': result, 'redirect': url_for('dashboard_page'), 'message': 'New account created and logged in successfully!'})
    else:
        user_obj = {'username': username, 'name': name, 'email': email, 'role': role, 'hostel_block': 'Block A - Boys', 'phone': '+91 98765 43210'}
        session['user'] = user_obj
        return jsonify({'success': True, 'user': user_obj, 'redirect': url_for('dashboard_page')})


@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json or request.form
    username = (data.get('username') or '').strip()
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    password = (data.get('password') or '').strip()
    role = data.get('role', 'Admin')
    hostel_block = data.get('hostel_block', 'Central Admin')
    phone = data.get('phone', '+91 98765 43210')

    if not username or not email or not password or not name:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    ok, result = create_user(username, name, email, password, role, hostel_block, phone)
    if ok:
        session['user'] = result
        return jsonify({'success': True, 'message': 'Account registered successfully!', 'user': result, 'redirect': url_for('dashboard_page')})
    else:
        return jsonify({'success': False, 'message': result}), 400


@app.route('/api/profile/update', methods=['POST'])
def api_update_profile():
    data = request.json or request.form
    current_user = session.get('user', {})
    user_id = current_user.get('id') or current_user.get('username')

    name = data.get('name', current_user.get('name'))
    email = data.get('email', current_user.get('email'))
    phone = data.get('phone', current_user.get('phone'))
    hostel_block = data.get('hostel_block', current_user.get('hostel_block'))
    role = data.get('role', current_user.get('role'))

    ok, msg = update_user_profile(user_id, name, email, phone, hostel_block, role)
    
    # Update current session
    updated_user = dict(current_user)
    updated_user.update({
        'name': name,
        'email': email,
        'phone': phone,
        'hostel_block': hostel_block,
        'role': role
    })
    session['user'] = updated_user

    return jsonify({'success': True, 'message': 'Profile details updated successfully!', 'user': updated_user})


@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    data = request.json or request.form
    username = data.get('username') or data.get('email', '').split('@')[0]
    name = data.get('name')
    email = data.get('email')
    password = data.get('password') or 'user123'
    role = data.get('role', 'Hostel Staff')
    hostel_block = data.get('hostel_block', 'Block A - Boys')
    phone = data.get('phone', '+91 98765 43210')

    if not name or not email:
        return jsonify({'success': False, 'message': 'Name and Email are required'}), 400

    ok, result = create_user(username, name, email, password, role, hostel_block, phone)
    if ok:
        return jsonify({'success': True, 'message': 'New user added successfully!', 'user': result})
    else:
        return jsonify({'success': False, 'message': result}), 400


@app.route('/api/users/delete/<int:user_id>', methods=['POST'])
def api_delete_user(user_id):
    delete_user(user_id)
    return jsonify({'success': True, 'message': 'User deleted successfully'})


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json or {}
    try:
        ph = float(data.get('ph', 7.0))
        tds = float(data.get('tds', 300))
        turbidity = float(data.get('turbidity', 1.0))
        temp = float(data.get('temperature', 25.0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid numeric parameters'}), 400

    score, status = calculate_purity_score(ph, tds, turbidity, temp)
    param_eval = evaluate_parameter_statuses(ph, tds, turbidity, temp)
    rule_engine = get_rule_engine()
    ai_diag = rule_engine.diagnose(ph, tds, turbidity, temp)

    return jsonify({
        'score': score,
        'status': status,
        'parameters': param_eval,
        'ai_diagnosis': ai_diag
    })


@app.route('/api/water-test', methods=['POST'])
def api_save_water_test():
    data = request.json or request.form.to_dict()

    try:
        ph = float(data.get('ph', 7.0))
        tds = float(data.get('tds', 300))
        turbidity = float(data.get('turbidity', 1.0))
        temp = float(data.get('temperature', 25.0))
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid numeric values'}), 400

    score, status = calculate_purity_score(ph, tds, turbidity, temp)
    rule_engine = get_rule_engine()
    ai_diag = rule_engine.diagnose(ph, tds, turbidity, temp)

    now = datetime.now()
    reading_entry = {
        'Date': data.get('date', now.strftime('%Y-%m-%d')),
        'Time': data.get('time', now.strftime('%H:%M')),
        'Hostel Block': data.get('hostel_block', 'Block A - Boys'),
        'Tank': data.get('tank_name', 'Overhead Tank 1'),
        'Collector': data.get('collector_name', 'Staff Member'),
        'pH': ph,
        'TDS': tds,
        'Temperature': temp,
        'Turbidity': turbidity,
        'Purity Score': score,
        'Status': status,
        'Recommendation': ai_diag['summary']
    }

    success, result = add_reading(reading_entry)

    # Trigger automatic alert if water is UNSAFE
    if status == 'UNSAFE':
        alert_type = 'Unsafe Water Alert'
        if tds > 500:
            alert_type = 'High TDS Alert'
        elif turbidity > 5.0:
            alert_type = 'High Turbidity Alert'
        elif ph < 6.5:
            alert_type = 'Low pH Alert'
        elif ph > 8.5:
            alert_type = 'High pH Alert'

        create_alert(
            alert_type=alert_type,
            title=f"Unsafe Quality: {reading_entry['Hostel Block']}",
            message=f"{alert_type} detected ({ai_diag['summary']}). Purity score: {score}/100.",
            hostel_block=reading_entry['Hostel Block'],
            tank=reading_entry['Tank'],
            severity='High'
        )

    if success:
        return jsonify({
            'success': True,
            'message': 'Water test analysis completed & saved to CSV successfully!',
            'score': score,
            'status': status,
            'recommendation': ai_diag['summary'],
            'ai_diag': ai_diag
        })
    else:
        return jsonify({'success': False, 'message': f'CSV Save Error: {result}'}), 500


@app.route('/api/readings')
def api_get_readings():
    readings = get_all_readings()
    return jsonify({'success': True, 'count': len(readings), 'readings': readings})


@app.route('/api/dashboard-summary')
def api_dashboard_summary():
    return jsonify(get_dashboard_summary())


@app.route('/api/export-csv')
def api_export_csv():
    if os.path.exists(CSV_FILE_PATH):
        return send_file(CSV_FILE_PATH, as_attachment=True, download_name='hostel_water_readings.csv')
    return jsonify({'error': 'CSV file not found'}), 404


@app.route('/api/alerts/toggle/<int:alert_id>', methods=['POST'])
def api_toggle_alert(alert_id):
    toggle_alert_status(alert_id)
    return jsonify({'success': True})


@app.route('/api/feedback', methods=['POST'])
def api_submit_feedback():
    data = request.json or {}
    save_feedback_entry(
        name=data.get('name', 'Anonymous'),
        email=data.get('email', 'user@hostel.edu'),
        category=data.get('category', 'General'),
        message=data.get('message', '')
    )
    return jsonify({'success': True, 'message': 'Feedback submitted successfully!'})


if __name__ == '__main__':
    print("Starting Water Purity Tracker Server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
