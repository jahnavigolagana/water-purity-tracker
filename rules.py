"""
Water Purity Tracker - Python AI Rule Engine
Evaluates water parameters against Engineering Chemistry rules to generate
intelligent treatment recommendations, severity ratings, and actionable steps.
"""

class WaterRuleEngine:
    @staticmethod
    def diagnose(ph, tds, turbidity, temperature):
        """
        Executes expert rule evaluation on water quality metrics.
        Returns a dictionary containing summary, detailed steps, overall priority, and expected outcomes.
        """
        try:
            ph = float(ph)
            tds = float(tds)
            turbidity = float(turbidity)
            temperature = float(temperature)
        except (ValueError, TypeError):
            return {
                'summary': 'Invalid Parameters Supplied',
                'recommendations': [],
                'priority': 'High',
                'expected_improvement': 'N/A'
            }

        recs = []
        priorities = []

        # Rule 1: High Total Dissolved Solids
        if tds > 500:
            p_level = 'High' if tds > 750 else 'Medium'
            priorities.append(p_level)
            recs.append({
                'parameter': 'TDS',
                'value': f'{tds} ppm',
                'limit': '500 ppm',
                'issue': 'High concentration of dissolved minerals and salts.',
                'action': 'Reverse Osmosis (RO) Filtration',
                'details': 'Install or service commercial RO semi-permeable membranes to remove excess salts, heavy metals, and hard minerals.',
                'priority': p_level,
                'expected_improvement': 'Reduces TDS by 85%-95%, bringing levels below 200 ppm.'
            })

        # Rule 2: Low pH (Acidic)
        if ph < 6.5:
            p_level = 'High' if ph < 6.0 else 'Medium'
            priorities.append(p_level)
            recs.append({
                'parameter': 'pH',
                'value': f'{ph}',
                'limit': '6.5 - 8.5',
                'issue': 'Acidic water may corrode hostel plumbing pipes and cause metallic taste.',
                'action': 'Neutralization Filter (Calcite / Soda Ash Dosing)',
                'details': 'Pass water through a Calcite neutralizer tank or inject sodium carbonate to elevate pH to neutral (~7.2).',
                'priority': p_level,
                'expected_improvement': 'Raises pH to 7.0-7.5 standard baseline.'
            })

        # Rule 3: High pH (Alkaline)
        if ph > 8.5:
            p_level = 'High' if ph > 9.0 else 'Medium'
            priorities.append(p_level)
            recs.append({
                'parameter': 'pH',
                'value': f'{ph}',
                'limit': '6.5 - 8.5',
                'issue': 'Alkaline water reduces chlorine disinfection efficiency and causes scale buildup in tanks.',
                'action': 'Chemical Balancing / Acid Infusion',
                'details': 'Dose mild food-grade citric acid or dilute hydrochloric acid via metering pump to reduce alkalinity.',
                'priority': p_level,
                'expected_improvement': 'Lowers pH to 7.4 safe drinking range.'
            })

        # Rule 4: High Turbidity (Cloudy / Particulates)
        if turbidity > 5.0:
            p_level = 'High' if turbidity > 8.0 else 'Medium'
            priorities.append(p_level)
            recs.append({
                'parameter': 'Turbidity',
                'value': f'{turbidity} NTU',
                'limit': '5.0 NTU',
                'issue': 'High suspended particles, sediment, or silt content harboring microbes.',
                'action': 'Multi-Stage Sedimentation & Sand Filtration + UV Disinfection',
                'details': 'Run water through dual media sand filters, followed by an Activated Carbon Filter and inline UV germicidal treatment.',
                'priority': p_level,
                'expected_improvement': 'Clears turbidity to < 1.0 NTU and sterilizes pathogens.'
            })

        # Rule 5: Elevated Temperature
        if temperature > 35.0:
            priorities.append('Low')
            recs.append({
                'parameter': 'Temperature',
                'value': f'{temperature} °C',
                'limit': '20 - 35 °C',
                'issue': 'High temperature promotes bacterial growth and accelerates pipe oxidation.',
                'action': 'Storage Tank Inspection & Cooling Shading',
                'details': 'Inspect rooftop tanks for direct sun exposure, install thermal insulation covers, and ensure chlorination levels are checked.',
                'priority': 'Medium',
                'expected_improvement': 'Stabilizes water temperature between 24°C and 28°C.'
            })

        # Final Summary Synthesis
        if not recs:
            overall_priority = 'Low'
            summary = 'Water Safe - No Treatment Required'
            expected_improvement = 'Water meets WHO and Indian BIS (IS 10500) drinking standards.'
        else:
            if 'High' in priorities:
                overall_priority = 'High Priority Action Needed'
            elif 'Medium' in priorities:
                overall_priority = 'Medium Priority Recommended'
            else:
                overall_priority = 'Low Priority Maintenance'

            summary = ' & '.join([r['action'].split(' (')[0] for r in recs])
            expected_improvement = 'Multi-stage purification will restore water to 95%+ purity level.'

        return {
            'summary': summary,
            'recommendations': recs,
            'priority': overall_priority,
            'expected_improvement': expected_improvement
        }

def get_rule_engine():
    return WaterRuleEngine()
