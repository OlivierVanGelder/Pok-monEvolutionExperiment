import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def create_type_coverage_heatmap(team, type_effectiveness):
    """Create a heatmap showing team's type coverage"""
    # Get all Pokemon types
    all_types = list(type_effectiveness.keys())
    
    # Create coverage matrix
    coverage_matrix = []
    pokemon_names = []
    
    for pokemon in team:
        row = []
        for defending_type in all_types:
            effectiveness = type_effectiveness[pokemon['Type 1']][defending_type]
            if pd.notna(pokemon['Type 2']):
                second_effectiveness = type_effectiveness[pokemon['Type 2']][defending_type]
                effectiveness = max(effectiveness, second_effectiveness)
            row.append(effectiveness)
        coverage_matrix.append(row)
        pokemon_names.append(pokemon['Name'])
    
    # Create heatmap
    plt.figure(figsize=(15, len(team) * 0.5 + 2))
    sns.heatmap(coverage_matrix, 
                xticklabels=all_types,
                yticklabels=pokemon_names,
                cmap='RdYlGn',
                center=1.0,
                vmin=0,
                vmax=2,
                annot=True,
                fmt='.1f')
    
    plt.title("Team Type Coverage")
    plt.xlabel("Defending Type")
    plt.ylabel("Team Member")
    plt.xticks(rotation=45)
    return plt.gcf() 