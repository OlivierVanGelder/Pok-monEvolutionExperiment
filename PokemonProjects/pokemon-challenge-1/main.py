import argparse
import pandas as pd
from typing import List, Optional
from src.analyzer.evolution_analyzer import PokemonAnalyzer
from src.visualization.visualizer import PokemonVisualizer
import os

class PokemonCLI:
    def __init__(self):
        """Initialize CLI with Pokemon data"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(script_dir, 'data', 'pokemon.csv')
            self.analyzer = PokemonAnalyzer(data_path)
            self.visualizer = PokemonVisualizer()
        except Exception as e:
            print(f"Error loading Pokemon data: {e}")
            raise
        
    def run(self):
        """Main CLI loop"""
        print("\n=== Pokemon Evolution Analysis Tool ===")
        while True:
            print("\nAvailable commands:")
            print("1. analyze <pokemon_name> - Analyze evolution chain")
            print("2. compare <pokemon1> <pokemon2> - Compare two Pokemon")
            print("3. visualize <pokemon_name> - Create evolution visualizations")
            print("4. search <type/stat> <value> - Search Pokemon by type or stat")
            print("5. help - Show this menu")
            print("6. quit - Exit program")
            
            command = input("\nEnter command: ").strip().split()
            
            if not command:
                continue
                
            if command[0] == 'quit':
                break
            
            try:
                self._handle_command(command)
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _handle_command(self, command: List[str]):
        """Handle CLI commands"""
        cmd = command[0].lower()
        
        if cmd == 'analyze':
            if len(command) < 2:
                print("Please specify a Pokemon name")
                return
            pokemon = command[1].capitalize()
            self._show_analysis(pokemon)
            
        elif cmd == 'compare':
            if len(command) < 3:
                print("Please specify two Pokemon names")
                return
            pokemon1 = command[1].capitalize()
            pokemon2 = command[2].capitalize()
            self._compare_pokemon(pokemon1, pokemon2)
            
        elif cmd == 'visualize':
            if len(command) < 2:
                print("Please specify a Pokemon name")
                return
            pokemon = command[1].capitalize()
            self._show_visualizations(pokemon)
            
        elif cmd == 'search':
            if len(command) < 3:
                print("Please specify search criteria and value")
                return
            criteria = command[1].lower()
            value = command[2]
            self._search_pokemon(criteria, value)
            
        elif cmd == 'help':
            self._show_help()
            
        else:
            print("Unknown command. Type 'help' for available commands.")
    
    def _show_analysis(self, pokemon: str):
        """Display evolution chain analysis"""
        analysis = self.analyzer.analyze_evolution_chain(pokemon)
        print(f"\nEvolution Analysis for {pokemon}:")
        print("\nStat Changes:")
        for stage, stats in analysis['stat_changes'].items():
            print(f"\n{stage}:")
            for stat, change in stats.items():
                print(f"  {stat}: {change:+d}")
        
        print("\nType Advantages:")
        for stage, types in analysis['type_advantages'].items():
            print(f"\n{stage}: {', '.join(types)}")
    
    def _compare_pokemon(self, pokemon1: str, pokemon2: str):
        """Compare two Pokemon"""
        comparison = self.analyzer.compare_pokemon(pokemon1, pokemon2)
        print(f"\nComparison: {pokemon1} vs {pokemon2}")
        print("\nBase Stats:")
        for stat, values in comparison['stats'].items():
            print(f"{stat:10}: {pokemon1}: {values[0]:3d} | {pokemon2}: {values[1]:3d}")
        
        print("\nType Effectiveness:")
        for type_name, effectiveness in comparison['type_effectiveness'].items():
            print(f"{type_name:10}: {effectiveness}")
    
    def _show_visualizations(self, pokemon: str):
        """Display evolution visualizations"""
        try:
            print(f"\nGenerating visualizations for {pokemon}...")
            # Get Pokemon data in the correct format
            pokemon_data = {
                'stats': {},
                'evolution': {},
                'types': {},
                'battle': {}
            }
            
            # Get evolution chain data
            chain = self.analyzer._get_evolution_chain(pokemon)
            
            # Populate stats data for each Pokemon in chain
            for poke in chain:
                poke_stats = self.analyzer.df[self.analyzer.df['name'] == poke].iloc[0]
                pokemon_data['stats'][poke] = {
                    'hp': poke_stats['hp'],
                    'attack': poke_stats['attack'],
                    'defense': poke_stats['defense'],
                    'sp_attack': poke_stats['sp_attack'],
                    'sp_defense': poke_stats['sp_defense'],
                    'speed': poke_stats['speed']
                }
                
                # Populate evolution data
                pokemon_data['evolution'][poke] = pokemon_data['stats'][poke]
            
            # Create type effectiveness matrix for heatmap
            type_cols = [col for col in self.analyzer.df.columns if col.startswith('against_')]
            type_data = {}
            for poke in chain:
                poke_data = self.analyzer.df[self.analyzer.df['name'] == poke].iloc[0]
                type_data[poke] = [poke_data[col] for col in type_cols]
            pokemon_data['types'] = pd.DataFrame(type_data, 
                                               index=[col.replace('against_', '') for col in type_cols])
            
            # Add battle metrics
            pokemon_data['battle'] = {
                'Attack Power': pokemon_data['stats'][pokemon]['attack'],
                'Special Power': pokemon_data['stats'][pokemon]['sp_attack'],
                'Defense': pokemon_data['stats'][pokemon]['defense'],
                'Speed': pokemon_data['stats'][pokemon]['speed']
            }
            
            self.visualizer.create_evolution_dashboard(pokemon_data)
            
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _search_pokemon(self, criteria: str, value: str):
        """Search Pokemon by type or stat"""
        results = self.analyzer.search_pokemon(criteria, value)
        print(f"\nSearch results for {criteria}={value}:")
        for pokemon in results:
            print(f"- {pokemon['name']}: {pokemon['stats']}")
    
    def _show_help(self):
        """Display detailed help information"""
        print("\nDetailed Command Help:")
        print("\nanalyze <pokemon_name>")
        print("  Analyzes the complete evolution chain of the specified Pokemon")
        print("  Example: analyze charmander")
        
        print("\ncompare <pokemon1> <pokemon2>")
        print("  Compares two Pokemon's stats and type effectiveness")
        print("  Example: compare pikachu raichu")
        
        print("\nvisualize <pokemon_name>")
        print("  Creates visual representations of the Pokemon's evolution chain")
        print("  Example: visualize squirtle")
        
        print("\nsearch <type/stat> <value>")
        print("  Searches for Pokemon by type or minimum stat value")
        print("  Example: search type fire")
        print("  Example: search attack 100")

def main():
    """Entry point for the CLI application"""
    cli = PokemonCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        print("\nThanks for using Pokemon Evolution Analysis Tool!")

if __name__ == "__main__":
    main() 