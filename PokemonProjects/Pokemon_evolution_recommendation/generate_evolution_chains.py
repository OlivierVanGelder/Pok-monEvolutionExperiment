import pandas as pd
import json
import os

def get_base_name(name):
    """Get base name for evolution matching"""
    # Common evolution patterns
    if name.endswith(('-O', '-M', ' X', ' Y', '-Attack', '-Defense', '-Speed', '-Sandy', '-Trash')):
        return name.split('-')[0].strip()
    return name

def generate_evolution_chains(df):
    """Generate evolution chains based on name patterns and stats"""
    evolution_chains = {}
    processed = set()
    
    # Sort by pokedex number to maintain order
    df = df.sort_values('pokedex_number')
    
    for _, pokemon in df.iterrows():
        name = pokemon['name'].upper()
        if name in processed:
            continue
            
        base_name = get_base_name(name)
        base_stats = pokemon['base_total']
        
        # Find potential evolutions
        potential_evos = df[
            (df['base_total'] > base_stats) & 
            (df['type1'] == pokemon['type1']) &  # Same primary type
            (df['generation'] == pokemon['generation'])  # Same generation
        ].sort_values('base_total')
        
        chain = [name]
        processed.add(name)
        
        for _, evo in potential_evos.iterrows():
            evo_name = evo['name'].upper()
            if evo_name not in processed and (
                evo_name.startswith(base_name[:4]) or  # Name pattern match
                evo['base_total'] - base_stats < 100    # Reasonable stat increase
            ):
                chain.append(evo_name)
                processed.add(evo_name)
                base_stats = evo['base_total']
        
        if len(chain) > 1:  # Only add if there's an evolution
            evolution_chains[name] = chain
            # Add entries for middle evolutions
            for i in range(1, len(chain)-1):
                evolution_chains[chain[i]] = chain[i:]
    
    return evolution_chains

def save_evolution_chains():
    """Generate and save evolution chains to JSON"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'pokemon.csv')
    json_path = os.path.join(script_dir, 'evolution_chains.json')
    
    try:
        df = pd.read_csv(csv_path)
        print(f"Generating evolution chains for {len(df)} Pokemon...")
        
        chains = generate_evolution_chains(df)
        
        with open(json_path, 'w') as f:
            json.dump(chains, f, indent=2)
        
        print(f"Successfully saved {len(chains)} evolution chains to {json_path}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    save_evolution_chains() 