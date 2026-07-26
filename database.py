"""
Water Purity Tracker - Database & In-Memory Store
Manages user credentials, role authorization, alert logs, settings, and feedback entries.
"""

import sqlite3
import os
from datetime import datetime



DB_PATH = "/tmp/water_purity.db"
def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes tables and seeds default admin, staff, and student accounts."""
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Student',
            hostel_block TEXT DEFAULT 'Block A - Boys',
            phone TEXT DEFAULT '+91 98765 43210',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            hostel_block TEXT NOT NULL,
            tank TEXT NOT NULL,
            severity TEXT NOT NULL,
            resolved INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,
            dark_mode INTEGER DEFAULT 0,
            theme TEXT DEFAULT 'ocean',
            notifications INTEGER DEFAULT 1,
            email_alerts INTEGER DEFAULT 1,
            language TEXT DEFAULT 'English'
        )
    ''')

    # Feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            category TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed Default Users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO users (username, name, email, password, role, hostel_block, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', [
            ('admin', 'Dr. Rajesh Sharma', 'admin@hostel.edu', 'admin123', 'Admin', 'Central Admin', '+91 98765 11111'),
            ('staff', 'Suresh Verma', 'staff@hostel.edu', 'staff123', 'Hostel Staff', 'Block B - Boys', '+91 98765 22222'),
            ('student', 'Rahul Verma', 'student@hostel.edu', 'student123', 'Student', 'Block A - Boys', '+91 98765 33333')
        ])

    # Seed Initial Alerts if empty
    cursor.execute("SELECT COUNT(*) FROM alerts")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO alerts (alert_type, title, message, hostel_block, tank, severity, resolved, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', [
            ('High TDS', 'Critical TDS Level Detected', 'TDS reached 720 ppm in Borewell Tank.', 'Block D - PG', 'Borewell Tank', 'High', 0, '2026-07-22 12:00:00'),
            ('Low pH', 'Acidic Water Alert', 'pH dropped to 5.9 in Underground Sump.', 'Block C - Girls', 'Underground Sump', 'High', 0, '2026-07-18 11:15:00'),
            ('High Turbidity', 'Turbidity Out of Safe Range', 'Turbidity recorded at 6.5 NTU.', 'Block B - Boys', 'Underground Sump', 'Medium', 1, '2026-07-25 09:15:00'),
            ('High pH', 'Alkaline Spike Warning', 'pH recorded at 8.8 in Overhead Tank 2.', 'Block A - Boys', 'Overhead Tank 2', 'Medium', 1, '2026-07-24 08:45:00')
        ])

    conn.commit()
    conn.close()

def get_all_users():
    conn = get_db()
    users = conn.execute("SELECT * FROM users ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(u) for u in users]

def get_alerts_list():
    conn = get_db()
    alerts = conn.execute("SELECT * FROM alerts ORDER BY timestamp DESC").fetchall()
    conn.close()
    return [dict(a) for a in alerts]

def toggle_alert_status(alert_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE alerts SET resolved = CASE WHEN resolved = 1 THEN 0 ELSE 1 END WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
    return True

def create_alert(alert_type, title, message, hostel_block, tank, severity):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (alert_type, title, message, hostel_block, tank, severity, resolved)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    ''', (alert_type, title, message, hostel_block, tank, severity))
    conn.commit()
    conn.close()

def save_feedback_entry(name, email, category, message):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (name, email, category, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, category, message))
    conn.commit()
    conn.close()

def create_user(username, name, email, password, role='Hostel Staff', hostel_block='Block A - Boys', phone='+91 98765 43210'):
    """Inserts a new user into SQLite database."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, name, email, password, role, hostel_block, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, name, email, password, role, hostel_block, phone))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, {'id': user_id, 'username': username, 'name': name, 'email': email, 'role': role, 'hostel_block': hostel_block, 'phone': phone}
    except sqlite3.IntegrityError as e:
        conn.close()
        return False, 'Username or Email already registered'

def update_user_profile(username_or_id, name, email, phone, hostel_block, role=None):
    """Updates user profile details in SQLite database."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        if isinstance(username_or_id, int) or str(username_or_id).isdigit():
            if role:
                cursor.execute('''
                    UPDATE users SET name = ?, email = ?, phone = ?, hostel_block = ?, role = ? WHERE id = ?
                ''', (name, email, phone, hostel_block, role, username_or_id))
            else:
                cursor.execute('''
                    UPDATE users SET name = ?, email = ?, phone = ?, hostel_block = ? WHERE id = ?
                ''', (name, email, phone, hostel_block, username_or_id))
        else:
            if role:
                cursor.execute('''
                    UPDATE users SET name = ?, email = ?, phone = ?, hostel_block = ?, role = ? WHERE username = ? OR email = ?
                ''', (name, email, phone, hostel_block, role, username_or_id, username_or_id))
            else:
                cursor.execute('''
                    UPDATE users SET name = ?, email = ?, phone = ?, hostel_block = ? WHERE username = ? OR email = ?
                ''', (name, email, phone, hostel_block, username_or_id, username_or_id))
        conn.commit()
        conn.close()
        return True, "Profile updated successfully"
    except Exception as e:
        conn.close()
        return False, str(e)

def delete_user(user_id):
    """Deletes a user account from database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True
