import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class PokemonAnalyzer:
    def __init__(self, data_path: str):
        """Initialize the analyzer with Pokemon data"""
        self.df = pd.read_csv(data_path)
        self.stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    
    def analyze_evolution_chain(self, pokemon: str) -> Dict:
        """Analyze the evolution chain of a Pokemon"""
        # Get the evolution chain (simplified for demonstration)
        chain = self._get_evolution_chain(pokemon)
        
        stat_changes = {}
        type_advantages = {}
        
        # Calculate changes between evolution stages
        for i in range(len(chain) - 1):
            base = chain[i]
            evolved = chain[i + 1]
            
            changes = self._calculate_stat_changes(base, evolved)
            stat_changes[f"{base} → {evolved}"] = changes
            
            type_advantages[base] = self._get_type_advantages(base)
            type_advantages[evolved] = self._get_type_advantages(evolved)
        
        return {
            'stat_changes': stat_changes,
            'type_advantages': type_advantages
        }
    
    def compare_pokemon(self, pokemon1: str, pokemon2: str) -> Dict:
        """Compare two Pokemon's stats and type effectiveness"""
        p1 = self.df[self.df['name'] == pokemon1].iloc[0]
        p2 = self.df[self.df['name'] == pokemon2].iloc[0]
        
        stats_comparison = {}
        for stat in self.stats:
            stats_comparison[stat] = [p1[stat], p2[stat]]
        
        type_effectiveness = self._compare_type_effectiveness(p1, p2)
        
        return {
            'stats': stats_comparison,
            'type_effectiveness': type_effectiveness
        }
    
    def search_pokemon(self, criteria: str, value: str) -> List[Dict]:
        """Search Pokemon by type or minimum stat value"""
        if criteria == 'type':
            matches = self.df[
                (self.df['type1'] == value) | 
                (self.df['type2'] == value)
            ]
        else:  # stat search
            try:
                min_value = int(value)
                matches = self.df[self.df[criteria] >= min_value]
            except ValueError:
                return []
        
        results = []
        for _, pokemon in matches.iterrows():
            stats = {stat: pokemon[stat] for stat in self.stats}
            results.append({
                'name': pokemon['name'],
                'stats': stats
            })
        
        return results
    
    def _get_evolution_chain(self, pokemon: str) -> List[str]:
        """Get the evolution chain for a Pokemon"""
        # Simplified evolution chains for demonstration
        evolution_chains = {
            'Charmander': ['Charmander', 'Charmeleon', 'Charizard'],
            'Bulbasaur': ['Bulbasaur', 'Ivysaur', 'Venusaur'],
            'Squirtle': ['Squirtle', 'Wartortle', 'Blastoise']
            # Add more evolution chains as needed
        }
        
        for chain in evolution_chains.values():
            if pokemon in chain:
                return chain[chain.index(pokemon):]
        
        return [pokemon]  # Return single Pokemon if no evolution chain found
    
    def _calculate_stat_changes(self, base: str, evolved: str) -> Dict[str, int]:
        """Calculate stat changes between two evolution stages"""
        base_stats = self.df[self.df['name'] == base].iloc[0]
        evolved_stats = self.df[self.df['name'] == evolved].iloc[0]
        
        changes = {}
        for stat in self.stats:
            changes[stat] = evolved_stats[stat] - base_stats[stat]
        
        return changes
    
    def _get_type_advantages(self, pokemon: str) -> List[str]:
        """Get type advantages for a Pokemon"""
        pokemon_data = self.df[self.df['name'] == pokemon].iloc[0]
        advantages = []
        
        for col in self.df.columns:
            if col.startswith('against_') and pokemon_data[col] < 1:
                type_name = col.replace('against_', '')
                advantages.append(type_name)
        
        return advantages
    
    def _compare_type_effectiveness(self, p1: pd.Series, p2: pd.Series) -> Dict[str, float]:
        """Compare type effectiveness between two Pokemon"""
        effectiveness = {}
        for col in self.df.columns:
            if col.startswith('against_'):
                type_name = col.replace('against_', '')
                effectiveness[type_name] = p1[col] / p2[col]
        
        return effectiveness