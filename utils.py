"""
Water Purity Tracker - Chemistry Standards & Utility Functions
Provides standards validation, purity score calculation, and helper formatting.
"""

SAFE_STANDARDS = {
    'ph': {'min': 6.5, 'max': 8.5, 'unit': ''},
    'tds': {'min': 0, 'max': 500, 'unit': 'ppm'},
    'turbidity': {'min': 0, 'max': 5.0, 'unit': 'NTU'},
    'temperature': {'min': 20.0, 'max': 35.0, 'unit': '°C'}
}

def calculate_purity_score(ph, tds, turbidity, temperature):
    """
    Calculates a weighted Purity Score out of 100.
    - pH optimal range: 6.5 - 8.5 (Weight: 30%)
    - TDS optimal range: 0 - 500 ppm (Weight: 30%)
    - Turbidity optimal range: 0 - 5 NTU (Weight: 25%)
    - Temperature optimal range: 20 - 35°C (Weight: 15%)
    """
    try:
        ph = float(ph)
        tds = float(tds)
        turbidity = float(turbidity)
        temperature = float(temperature)
    except (ValueError, TypeError):
        return 0, 'UNSAFE'

    # pH score (30 points)
    if 6.5 <= ph <= 8.5:
        ph_score = 30
    elif 6.0 <= ph < 6.5 or 8.5 < ph <= 9.0:
        ph_score = 18
    elif 5.5 <= ph < 6.0 or 9.0 < ph <= 9.5:
        ph_score = 10
    else:
        ph_score = 0

    # TDS score (30 points)
    if tds <= 300:
        tds_score = 30
    elif 300 < tds <= 500:
        tds_score = 25
    elif 500 < tds <= 750:
        tds_score = 12
    elif 750 < tds <= 1000:
        tds_score = 5
    else:
        tds_score = 0

    # Turbidity score (25 points)
    if turbidity <= 1.0:
        turbidity_score = 25
    elif 1.0 < turbidity <= 5.0:
        turbidity_score = 20
    elif 5.0 < turbidity <= 8.0:
        turbidity_score = 10
    else:
        turbidity_score = 0

    # Temperature score (15 points)
    if 20.0 <= temperature <= 30.0:
        temp_score = 15
    elif 30.0 < temperature <= 35.0:
        temp_score = 12
    elif 15.0 <= temperature < 20.0 or 35.0 < temperature <= 40.0:
        temp_score = 6
    else:
        temp_score = 0

    total_score = round(ph_score + tds_score + turbidity_score + temp_score)
    total_score = max(0, min(100, total_score))

    # Water is SAFE if score >= 75 and no severe breach
    is_safe = (
        total_score >= 75 and
        (6.0 <= ph <= 8.8) and
        (tds <= 550) and
        (turbidity <= 5.5)
    )
    status = 'SAFE' if is_safe else 'UNSAFE'

    return total_score, status

def evaluate_parameter_statuses(ph, tds, turbidity, temperature):
    """
    Returns parameter-by-parameter compliance dictionary.
    """
    return {
        'ph': {
            'value': ph,
            'range': '6.5 - 8.5',
            'status': 'SAFE' if 6.5 <= ph <= 8.5 else ('WARNING' if 6.0 <= ph <= 9.0 else 'DANGER'),
            'message': 'Optimal pH' if 6.5 <= ph <= 8.5 else ('Slightly Acidic/Alkaline' if 6.0 <= ph <= 9.0 else 'Severely Off-balance')
        },
        'tds': {
            'value': tds,
            'range': '0 - 500 ppm',
            'status': 'SAFE' if tds <= 500 else ('WARNING' if tds <= 750 else 'DANGER'),
            'message': 'Low/Moderate Dissolved Solids' if tds <= 500 else 'High Dissolved Solid Concentration'
        },
        'turbidity': {
            'value': turbidity,
            'range': '0 - 5 NTU',
            'status': 'SAFE' if turbidity <= 5.0 else ('WARNING' if turbidity <= 8.0 else 'DANGER'),
            'message': 'Clear Water' if turbidity <= 5.0 else 'High Suspended Particulates / Cloudiness'
        },
        'temperature': {
            'value': temperature,
            'range': '20 - 35 °C',
            'status': 'SAFE' if 20.0 <= temperature <= 35.0 else 'WARNING',
            'message': 'Normal Temperature' if 20.0 <= temperature <= 35.0 else 'Elevated Water Temp'
        }
    }
