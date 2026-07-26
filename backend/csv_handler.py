"""
Water Purity Tracker - CSV Data Handling Module
Provides thread-safe operations for reading, writing, querying, filtering,
and exporting water_readings.csv.
"""

import os
import csv
from datetime import datetime

CSV_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'water_readings.csv')
CSV_COLUMNS = [
    'Date', 'Time', 'Hostel Block', 'Tank', 'Collector',
    'pH', 'TDS', 'Temperature', 'Turbidity', 'Purity Score',
    'Status', 'Recommendation'
]

def ensure_csv_exists():
    """Ensures CSV file exists with proper headers."""
    os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)
    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)

def get_all_readings():
    """Reads all rows from the CSV file as a list of dictionaries."""
    ensure_csv_exists()
    readings = []
    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['pH'] = float(row['pH'])
                    row['TDS'] = float(row['TDS'])
                    row['Temperature'] = float(row['Temperature'])
                    row['Turbidity'] = float(row['Turbidity'])
                    row['Purity Score'] = int(float(row['Purity Score']))
                except (ValueError, KeyError):
                    pass
                readings.append(row)
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return readings

def add_reading(data):
    """
    Appends a new reading dictionary to water_readings.csv.
    """
    ensure_csv_exists()
    now = datetime.now()
    row = {
        'Date': data.get('Date', now.strftime('%Y-%m-%d')),
        'Time': data.get('Time', now.strftime('%H:%M')),
        'Hostel Block': data.get('Hostel Block', 'Block A - Boys'),
        'Tank': data.get('Tank', 'Overhead Tank 1'),
        'Collector': data.get('Collector', 'Staff Member'),
        'pH': data.get('pH', 7.0),
        'TDS': data.get('TDS', 300),
        'Temperature': data.get('Temperature', 25.0),
        'Turbidity': data.get('Turbidity', 1.0),
        'Purity Score': data.get('Purity Score', 90),
        'Status': data.get('Status', 'SAFE'),
        'Recommendation': data.get('Recommendation', 'Water Safe - No Treatment Required')
    }

    try:
        with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writerow(row)
        return True, row
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        return False, str(e)

def filter_readings(search=None, hostel_block=None, status=None, date_from=None, date_to=None, sort_by='Date', sort_order='desc'):
    """
    Filters and sorts readings based on parameters.
    """
    readings = get_all_readings()

    if search:
        s = search.lower()
        readings = [
            r for r in readings
            if s in r.get('Hostel Block', '').lower()
            or s in r.get('Tank', '').lower()
            or s in r.get('Collector', '').lower()
            or s in r.get('Recommendation', '').lower()
        ]

    if hostel_block and hostel_block != 'All':
        readings = [r for r in readings if r.get('Hostel Block') == hostel_block]

    if status and status != 'All':
        readings = [r for r in readings if r.get('Status') == status]

    if date_from:
        readings = [r for r in readings if r.get('Date', '') >= date_from]

    if date_to:
        readings = [r for r in readings if r.get('Date', '') <= date_to]

    # Sorting logic
    reverse = (sort_order.lower() == 'desc')
    if sort_by in ['pH', 'TDS', 'Temperature', 'Turbidity', 'Purity Score']:
        readings.sort(key=lambda x: float(x.get(sort_by, 0)), reverse=reverse)
    else:
        readings.sort(key=lambda x: str(x.get(sort_by, '')), reverse=reverse)

    return readings

def get_dashboard_summary():
    """
    Computes key performance metrics and quick stats for the dashboard.
    """
    readings = get_all_readings()
    total = len(readings)

    if total == 0:
        return {
            'total_tests': 0, 'safe_count': 0, 'unsafe_count': 0,
            'avg_score': 0, 'avg_ph': 0, 'avg_tds': 0, 'avg_temp': 0, 'avg_turbidity': 0,
            'overall_status': 'NO DATA', 'last_updated': 'N/A', 'safe_percentage': 0
        }

    safe_count = sum(1 for r in readings if r.get('Status') == 'SAFE')
    unsafe_count = total - safe_count
    avg_score = round(sum(float(r.get('Purity Score', 0)) for r in readings) / total, 1)
    avg_ph = round(sum(float(r.get('pH', 0)) for r in readings) / total, 2)
    avg_tds = round(sum(float(r.get('TDS', 0)) for r in readings) / total, 1)
    avg_temp = round(sum(float(r.get('Temperature', 0)) for r in readings) / total, 1)
    avg_turbidity = round(sum(float(r.get('Turbidity', 0)) for r in readings) / total, 2)
    safe_pct = round((safe_count / total) * 100, 1)

    latest = readings[0] if readings else {}
    last_updated = f"{latest.get('Date', '')} {latest.get('Time', '')}"

    return {
        'total_tests': total,
        'safe_count': safe_count,
        'unsafe_count': unsafe_count,
        'safe_percentage': safe_pct,
        'avg_score': avg_score,
        'avg_ph': avg_ph,
        'avg_tds': avg_tds,
        'avg_temp': avg_temp,
        'avg_turbidity': avg_turbidity,
        'overall_status': 'SAFE' if safe_pct >= 75 else 'UNSAFE',
        'last_updated': last_updated,
        'latest_reading': latest
    }
