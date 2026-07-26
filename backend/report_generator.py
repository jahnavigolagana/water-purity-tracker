"""
Water Purity Tracker - Report Generation Engine
Computes analytical breakdowns for Daily, Weekly, Monthly, and Yearly reports.
"""

from datetime import datetime, timedelta
from backend.csv_handler import get_all_readings

def generate_period_report(period='weekly', hostel_block='All'):
    """
    Aggregates water quality metrics over specified timeframe (daily, weekly, monthly, yearly).
    """
    readings = get_all_readings()
    if hostel_block and hostel_block != 'All':
        readings = [r for r in readings if r.get('Hostel Block') == hostel_block]

    now = datetime.now()

    # Filter date range
    if period == 'daily':
        target_date = now.strftime('%Y-%m-%d')
        filtered = [r for r in readings if r.get('Date') == target_date]
        if not filtered:  # Fallback to recent date if no test today
            filtered = readings[:5]
        title = f"Daily Water Quality Report ({now.strftime('%d %b %Y')})"
    elif period == 'weekly':
        seven_days_ago = (now - timedelta(days=7)).strftime('%Y-%m-%d')
        filtered = [r for r in readings if r.get('Date', '') >= seven_days_ago]
        title = "Weekly Water Quality Audit Report (Past 7 Days)"
    elif period == 'monthly':
        thirty_days_ago = (now - timedelta(days=30)).strftime('%Y-%m-%d')
        filtered = [r for r in readings if r.get('Date', '') >= thirty_days_ago]
        title = "Monthly Water Quality Compliance Report"
    else:  # yearly
        one_year_ago = (now - timedelta(days=365)).strftime('%Y-%m-%d')
        filtered = [r for r in readings if r.get('Date', '') >= one_year_ago]
        title = "Annual Water Quality Executive Report"

    count = len(filtered)
    if count == 0:
        return {
            'title': title, 'period': period, 'total_tests': 0, 'safe_count': 0, 'unsafe_count': 0,
            'avg_ph': 0, 'avg_tds': 0, 'avg_temp': 0, 'avg_turbidity': 0, 'avg_score': 0,
            'compliance_rate': 0, 'block_summary': {}, 'readings': []
        }

    safe_count = sum(1 for r in filtered if r.get('Status') == 'SAFE')
    unsafe_count = count - safe_count
    avg_ph = round(sum(float(r.get('pH', 0)) for r in filtered) / count, 2)
    avg_tds = round(sum(float(r.get('TDS', 0)) for r in filtered) / count, 1)
    avg_temp = round(sum(float(r.get('Temperature', 0)) for r in filtered) / count, 1)
    avg_turbidity = round(sum(float(r.get('Turbidity', 0)) for r in filtered) / count, 2)
    avg_score = round(sum(float(r.get('Purity Score', 0)) for r in filtered) / count, 1)

    # Block level breakdown
    blocks = {}
    for r in filtered:
        b = r.get('Hostel Block', 'Unknown')
        if b not in blocks:
            blocks[b] = {'total': 0, 'safe': 0, 'unsafe': 0, 'scores': []}
        blocks[b]['total'] += 1
        if r.get('Status') == 'SAFE':
            blocks[b]['safe'] += 1
        else:
            blocks[b]['unsafe'] += 1
        blocks[b]['scores'].append(float(r.get('Purity Score', 0)))

    for b, data in blocks.items():
        data['avg_score'] = round(sum(data['scores']) / len(data['scores']), 1) if data['scores'] else 0
        data['safe_percentage'] = round((data['safe'] / data['total']) * 100, 1)

    return {
        'title': title,
        'period': period,
        'generated_on': now.strftime('%Y-%m-%d %H:%M:%S'),
        'total_tests': count,
        'safe_count': safe_count,
        'unsafe_count': unsafe_count,
        'compliance_rate': round((safe_count / count) * 100, 1),
        'avg_ph': avg_ph,
        'avg_tds': avg_tds,
        'avg_temp': avg_temp,
        'avg_turbidity': avg_turbidity,
        'avg_score': avg_score,
        'block_summary': blocks,
        'readings': filtered
    }
