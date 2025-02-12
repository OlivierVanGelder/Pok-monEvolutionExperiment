# Pokemon Evolution Analysis Tool

A comprehensive Pokemon analysis tool that helps trainers make informed decisions about Pokemon evolution and battle strategies.

## Features

### Command Line Interface

The tool provides an interactive CLI with the following commands:

1. `analyze <pokemon_name>` - Analyze evolution chain
2. `compare <pokemon1> <pokemon2>` - Compare two Pokemon
3. `visualize <pokemon_name>` - Create evolution visualizations
4. `search <type/stat> <value>` - Search Pokemon by type or stat
5. `help` - Show help menu
6. `quit` - Exit program

### Visualization Suite

The tool creates comprehensive visualizations for Pokemon analysis:

![Pokemon Analysis Dashboard](visualization_example.png)

The dashboard includes:

1. **Stat Radar Chart** - Compare stats across evolution stages
2. **Stat Progression** - Track stat changes through evolution
3. **Type Effectiveness Heatmap** - Analyze type matchups
4. **Battle Performance Metrics** - View key battle statistics

## Project Structure

```
pokemon-challenge-1/
├── src/
│   ├── analyzer/
│   │   └── evolution_analyzer.py
│   └── visualization/
│       └── visualizer.py
├── data/
│   └── pokemon.csv
├── main.py
└── README.md
```

## Components

### PokemonAnalyzer

-   Handles Pokemon data analysis
-   Calculates evolution chain statistics
-   Compares Pokemon stats and type effectiveness
-   Provides search functionality

### PokemonVisualizer

-   Creates radar charts for stat comparison
-   Generates evolution progression plots
-   Produces type effectiveness heatmaps
-   Shows battle performance metrics

## Usage

1. Make sure you have the required Pokemon dataset in `data/pokemon.csv`
2. Run the program:

```bash
python main.py
```

3. Use the interactive CLI to analyze Pokemon:

```bash
Enter command: visualize charmander
```

## Dependencies

-   Python 3.x
-   pandas
-   matplotlib
-   seaborn
-   numpy

## Data Source

The analysis uses the Complete Pokemon Dataset, which includes:

-   Base stats for all Pokemon
-   Evolution chains
-   Type information
-   Combat-relevant attributes

## Example Output

As shown in the visualization example:

-   The radar chart compares stats between evolution stages
-   The line graph shows stat progression through evolution
-   The heatmap displays type effectiveness
-   The bar chart shows battle performance metrics

This tool helps trainers understand:

-   How stats change during evolution
-   When to evolve their Pokemon
-   Type advantages and disadvantages
-   Battle performance implications
