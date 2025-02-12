import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict

class PokemonVisualizer:
    def __init__(self):
        """Initialize the visualizer"""
        self.stats = ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']
        # Set the style once during initialization
        plt.style.use('default')  # Using default style instead of seaborn
        sns.set_theme()  # This will apply seaborn styling
    
    def create_evolution_dashboard(self, pokemon_data: Dict) -> None:
        """Create comprehensive evolution analysis dashboard"""
        fig = plt.figure(figsize=(15, 10))
        
        # 1. Stat Radar Chart
        ax1 = fig.add_subplot(221, projection='polar')
        self._create_stat_radar(pokemon_data['stats'], ax1)
        
        # 2. Evolution Progression
        ax2 = fig.add_subplot(222)
        self._create_stat_progression(pokemon_data['evolution'], ax2)
        
        # 3. Type Effectiveness Heatmap
        ax3 = fig.add_subplot(223)
        self._create_type_heatmap(pokemon_data['types'], ax3)
        
        # 4. Battle Performance
        ax4 = fig.add_subplot(224)
        self._create_battle_metrics(pokemon_data['battle'], ax4)
        
        plt.tight_layout()
        plt.show()
    
    def _create_stat_radar(self, stats_data: Dict, ax) -> None:
        """Create radar chart for Pokemon stats"""
        angles = np.linspace(0, 2*np.pi, len(self.stats), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))  # Complete the circle
        
        for pokemon, stats in stats_data.items():
            values = [stats[stat.lower().replace('. ', '_')] for stat in self.stats]
            values = np.concatenate((values, [values[0]]))
            
            ax.plot(angles, values, 'o-', linewidth=2, label=pokemon)
            ax.fill(angles, values, alpha=0.25)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.stats)
        ax.set_title('Stat Comparison')
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    def _create_stat_progression(self, evolution_data: Dict, ax) -> None:
        """Create line plot showing stat progression through evolution"""
        stages = list(evolution_data.keys())
        stats = list(evolution_data[stages[0]].keys())
        
        for stat in stats:
            values = [evolution_data[stage][stat] for stage in stages]
            ax.plot(stages, values, marker='o', label=stat.upper())
        
        ax.set_title('Stat Progression Through Evolution')
        ax.set_xlabel('Evolution Stage')
        ax.set_ylabel('Stat Value')
        ax.legend()
        plt.setp(ax.get_xticklabels(), rotation=45)
    
    def _create_type_heatmap(self, type_data: Dict, ax) -> None:
        """Create type effectiveness heatmap"""
        sns.heatmap(
            data=type_data,
            annot=True,
            cmap='RdYlBu_r',
            center=1,
            ax=ax,
            fmt='.2f'
        )
        ax.set_title('Type Effectiveness')
        plt.setp(ax.get_xticklabels(), rotation=45)
        plt.setp(ax.get_yticklabels(), rotation=0)
    
    def _create_battle_metrics(self, battle_data: Dict, ax) -> None:
        """Create bar plot for battle performance metrics"""
        metrics = list(battle_data.keys())
        values = list(battle_data.values())
        
        ax.bar(metrics, values)
        ax.set_title('Battle Performance Metrics')
        ax.set_ylabel('Score')
        plt.setp(ax.get_xticklabels(), rotation=45)
    
    def create_comparison_plot(self, pokemon1: str, pokemon2: str, stats: Dict) -> None:
        """Create comparison plot for two Pokemon"""
        plt.figure(figsize=(10, 6))
        
        x = np.arange(len(self.stats))
        width = 0.35
        
        pokemon1_stats = [stats[stat.lower().replace('. ', '_')][0] for stat in self.stats]
        pokemon2_stats = [stats[stat.lower().replace('. ', '_')][1] for stat in self.stats]
        
        plt.bar(x - width/2, pokemon1_stats, width, label=pokemon1)
        plt.bar(x + width/2, pokemon2_stats, width, label=pokemon2)
        
        plt.xlabel('Stats')
        plt.ylabel('Value')
        plt.title(f'Stat Comparison: {pokemon1} vs {pokemon2}')
        plt.xticks(x, self.stats, rotation=45)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    def create_search_results_plot(self, results: List[Dict]) -> None:
        """Create visualization for search results"""
        if not results:
            return
        
        plt.figure(figsize=(12, 6))
        
        pokemon_names = [r['name'] for r in results]
        total_stats = [sum(r['stats'].values()) for r in results]
        
        plt.bar(pokemon_names, total_stats)
        plt.title('Total Stats Comparison')
        plt.xlabel('Pokemon')
        plt.ylabel('Total Stats')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show() 