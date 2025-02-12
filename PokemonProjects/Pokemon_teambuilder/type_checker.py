import json
import os
import pandas as pd

def load_type_effectiveness():
    """Load type effectiveness data from JSON"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'data', 'type_effectiveness.json')
    
    with open(json_path, 'r') as f:
        return json.load(f)

def get_team_coverage(team):
    """Calculate offensive type coverage of the team"""
    type_chart = load_type_effectiveness()
    coverage = {type_name: False for type_name in type_chart.keys()}
    
    for pokemon in team:
        # Check primary type coverage
        for target_type in coverage:
            if type_chart[pokemon['Type 1']][target_type] > 1:
                coverage[target_type] = True
        
        # Check secondary type coverage if it exists
        if pd.notna(pokemon['Type 2']):
            for target_type in coverage:
                if type_chart[pokemon['Type 2']][target_type] > 1:
                    coverage[target_type] = True
    
    return coverage

def get_team_weaknesses(team):
    """Calculate defensive weaknesses of the team"""
    type_chart = load_type_effectiveness()
    weaknesses = {}
    
    for pokemon in team:
        for attacking_type in type_chart:
            damage_multiplier = type_chart[attacking_type][pokemon['Type 1']]
            
            if pd.notna(pokemon['Type 2']):
                damage_multiplier *= type_chart[attacking_type][pokemon['Type 2']]
            
            if damage_multiplier > 1:
                weaknesses[attacking_type] = weaknesses.get(attacking_type, 0) + 1
    
    return {t: c for t, c in weaknesses.items() if c > 1}

def calculate_type_effectiveness(attacking_type, defending_pokemon):
    """Calculate effectiveness of an attack type against a Pokemon"""
    type_chart = load_type_effectiveness()
    
    effectiveness = type_chart[attacking_type][defending_pokemon['Type 1']]
    if pd.notna(defending_pokemon['Type 2']):
        effectiveness *= type_chart[attacking_type][defending_pokemon['Type 2']]
    
    return effectiveness 