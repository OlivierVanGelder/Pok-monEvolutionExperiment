import matplotlib.pyplot as plt
import numpy as np

def create_stat_radar(team, title="Team Stats Distribution"):
    """Create a radar chart showing team's stat distribution"""
    stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    
    # Calculate team averages
    avg_stats = []
    for stat in stats:
        avg = sum(p[stat] for p in team) / len(team)
        avg_stats.append(avg)
    
    # Number of variables
    num_vars = len(stats)
    
    # Compute angle for each axis
    angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
    angles += angles[:1]
    
    # Initialize the plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Plot data
    avg_stats += avg_stats[:1]
    ax.plot(angles, avg_stats, 'o-', linewidth=2, label='Team Average')
    ax.fill(angles, avg_stats, alpha=0.25)
    
    # Fix axis to go in the right order and start at 12 o'clock
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each angle and label
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stats)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.title(title)
    return fig 