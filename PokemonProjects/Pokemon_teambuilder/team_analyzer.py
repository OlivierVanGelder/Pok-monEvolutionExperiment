import pandas as pd
import numpy as np

def analyze_team(team):
    """Analyze team composition and return insights"""
    insights = []
    
    # Check physical/special balance
    phys_attackers = len([p for p in team if p['Attack'] > p['Sp. Atk']])
    spec_attackers = len(team) - phys_attackers
    
    if abs(phys_attackers - spec_attackers) > 2:
        insights.append(f"Team is heavily skewed towards {'physical' if phys_attackers > spec_attackers else 'special'} attackers")
    
    # Check speed tiers
    speeds = [p['Speed'] for p in team]
    if max(speeds) < 80:
        insights.append("Team lacks fast Pokemon")
    elif min(speeds) > 70:
        insights.append("Team might be too fast - consider adding bulkier Pokemon")
    
    # Check defensive coverage
    tanks = len([p for p in team if (p['Defense'] + p['Sp. Def']) > 160])
    if tanks < 2:
        insights.append("Team needs more defensive Pokemon")
    
    return insights

def suggest_improvements(team, pokemon_df):
    """Suggest Pokemon to improve team composition"""
    suggestions = []
    
    # Get team's current types
    team_types = []
    for pokemon in team:
        team_types.append(pokemon['Type 1'])
        if pd.notna(pokemon['Type 2']):
            team_types.append(pokemon['Type 2'])
    
    # Find missing important types
    important_types = ['Water', 'Fire', 'Ground', 'Flying', 'Steel']
    missing_types = [t for t in important_types if t not in team_types]
    
    if missing_types:
        suggestions.append(f"Consider adding a {'/'.join(missing_types)} type Pokemon")
    
    # Suggest based on stat deficiencies
    avg_stats = {
        'Speed': sum(p['Speed'] for p in team) / len(team),
        'Defense': sum(p['Defense'] for p in team) / len(team),
        'Sp. Def': sum(p['Sp. Def'] for p in team) / len(team)
    }
    
    if avg_stats['Speed'] < 70:
        fast_options = pokemon_df[pokemon_df['Speed'] > 100].sample(2)['Name'].tolist()
        suggestions.append(f"Add a fast Pokemon like {' or '.join(fast_options)}")
    
    if avg_stats['Defense'] < 75 and avg_stats['Sp. Def'] < 75:
        tank_options = pokemon_df[
            (pokemon_df['Defense'] > 90) & 
            (pokemon_df['Sp. Def'] > 90)
        ].sample(2)['Name'].tolist()
        suggestions.append(f"Add a defensive Pokemon like {' or '.join(tank_options)}")
    
    return suggestions 