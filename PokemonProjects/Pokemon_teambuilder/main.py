import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from team_analyzer import analyze_team, suggest_improvements
from type_checker import get_team_coverage, get_team_weaknesses, load_type_effectiveness
from visualizations.radar_chart import create_stat_radar
from visualizations.type_coverage import create_type_coverage_heatmap

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

class TeamBuilder:
    def __init__(self):
        """Initialize TeamBuilder with Pokemon data"""
        try:
            # Load directly from local file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, 'data', 'pokemon.csv')
            self.df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"Error loading Pokemon data: {e}")
            raise
        
        self.team = []
        self.MAX_TEAM_SIZE = 6
        self.type_chart = load_type_effectiveness()

    def add_pokemon(self, pokemon_name):
        """Add a Pokemon to the team"""
        if len(self.team) >= self.MAX_TEAM_SIZE:
            return "Team is already full!"
        
        pokemon = self.df[self.df['Name'].str.upper() == pokemon_name.upper()]
        if pokemon.empty:
            return f"Pokemon {pokemon_name} not found!"
        
        self.team.append(pokemon.iloc[0])
        return f"{pokemon_name} added to team!"

    def remove_pokemon(self, pokemon_name):
        """Remove a Pokemon from the team"""
        for i, pokemon in enumerate(self.team):
            if pokemon['Name'].upper() == pokemon_name.upper():
                self.team.pop(i)
                return f"{pokemon_name} removed from team!"
        return f"{pokemon_name} not found in team!"

    def display_team(self):
        """Display current team composition"""
        if not self.team:
            return "Team is empty!"
        
        print("\nCurrent Team:")
        print("-" * 50)
        for i, pokemon in enumerate(self.team, 1):
            types = f"{pokemon['Type 1']}"
            if pd.notna(pokemon['Type 2']):
                types += f"/{pokemon['Type 2']}"
            print(f"{i}. {pokemon['Name']} ({types})")

    def analyze_team(self):
        """Analyze current team composition"""
        if not self.team:
            return "Team is empty!"

        # Display team analysis
        print("\nTeam Analysis:")
        print("-" * 50)
        
        # Show type coverage
        coverage = get_team_coverage(self.team)
        print("\nType Coverage:")
        for type_name, covered in coverage.items():
            print(f"{type_name}: {'✓' if covered else '✗'}")
        
        # Show team weaknesses
        weaknesses = get_team_weaknesses(self.team)
        if weaknesses:
            print("\nTeam Weaknesses:")
            for type_name, count in weaknesses.items():
                print(f"⚠ {count} Pokemon weak to {type_name}")
        
        # Show suggestions
        suggestions = suggest_improvements(self.team, self.df)
        if suggestions:
            print("\nSuggested Improvements:")
            for suggestion in suggestions:
                print(f"• {suggestion}")

    def visualize_team(self):
        """Create and display team visualizations"""
        if not self.team:
            return "Team is empty!"

        # Create stat radar chart
        radar_fig = create_stat_radar(self.team)
        plt.figure(radar_fig.number)
        plt.show()

        # Create type coverage heatmap
        coverage_fig = create_type_coverage_heatmap(self.team, self.type_chart)
        plt.figure(coverage_fig.number)
        plt.show()

def main():
    builder = TeamBuilder()
    
    print("Welcome to Pokemon Team Builder!")
    print("\nCommands:")
    print("  add     - Add a Pokemon to your team")
    print("  remove  - Remove a Pokemon from your team")
    print("  display - Show current team")
    print("  analyze - Analyze team composition")
    print("  viz     - Show team visualizations")
    print("  quit    - Exit the program")
    
    while True:
        command = input("\nEnter command: ").lower()
        
        if command == 'quit':
            break
        elif command == 'add':
            pokemon = input("Enter Pokemon name: ").title()
            print(builder.add_pokemon(pokemon))
        elif command == 'remove':
            pokemon = input("Enter Pokemon name: ").title()
            print(builder.remove_pokemon(pokemon))
        elif command == 'display':
            builder.display_team()
        elif command == 'analyze':
            builder.analyze_team()
        elif command == 'viz':
            builder.visualize_team()
        else:
            print("Unknown command!")

    print("\nThanks for using Pokemon Team Builder!")

if __name__ == "__main__":
    main()
