"""
Pokemon evolution chains from generations 1-7.
Format: 'BASE_POKEMON': ['BASE_POKEMON', 'FIRST_EVOLUTION', 'FINAL_EVOLUTION']
"""
import json
import os

# Define special evolution chains that need manual specification
SPECIAL_CHAINS = {
    # Eevee and Eeveelutions
    'EEVEE': ['EEVEE', ['VAPOREON', 'JOLTEON', 'FLAREON', 'ESPEON', 'UMBREON', 'LEAFEON', 'GLACEON', 'SYLVEON']],
    'VAPOREON': ['VAPOREON'],
    'JOLTEON': ['JOLTEON'],
    'FLAREON': ['FLAREON'],
    'ESPEON': ['ESPEON'],
    'UMBREON': ['UMBREON'],
    'LEAFEON': ['LEAFEON'],
    'GLACEON': ['GLACEON'],
    'SYLVEON': ['SYLVEON'],
    
    # Tyrogue evolutions
    'TYROGUE': ['TYROGUE', ['HITMONLEE', 'HITMONCHAN', 'HITMONTOP']],
    'HITMONLEE': ['HITMONLEE'],
    'HITMONCHAN': ['HITMONCHAN'],
    'HITMONTOP': ['HITMONTOP'],
    
    # Split evolutions
    'ODDISH': ['ODDISH', 'GLOOM', ['VILEPLUME', 'BELLOSSOM']],
    'GLOOM': ['GLOOM', ['VILEPLUME', 'BELLOSSOM']],
    'VILEPLUME': ['VILEPLUME'],
    'BELLOSSOM': ['BELLOSSOM'],
    
    'POLIWAG': ['POLIWAG', 'POLIWHIRL', ['POLIWRATH', 'POLITOED']],
    'POLIWHIRL': ['POLIWHIRL', ['POLIWRATH', 'POLITOED']],
    'POLIWRATH': ['POLIWRATH'],
    'POLITOED': ['POLITOED'],
    
    # Regular evolution chains
    'BULBASAUR': ['BULBASAUR', 'IVYSAUR', 'VENUSAUR'],
    'IVYSAUR': ['IVYSAUR', 'VENUSAUR'],
    'VENUSAUR': ['VENUSAUR'],
    
    'CHARMANDER': ['CHARMANDER', 'CHARMELEON', 'CHARIZARD'],
    'CHARMELEON': ['CHARMELEON', 'CHARIZARD'],
    'CHARIZARD': ['CHARIZARD'],
    
    'SQUIRTLE': ['SQUIRTLE', 'WARTORTLE', 'BLASTOISE'],
    'WARTORTLE': ['WARTORTLE', 'BLASTOISE'],
    'BLASTOISE': ['BLASTOISE'],
    
    # Add more evolution chains as needed...
}

def get_evolution_chain(pokemon_name):
    """
    Get the evolution chain for a given Pokemon.
    Args:
        pokemon_name (str): Name of the Pokemon (case insensitive)
    Returns:
        list: Evolution chain or None if not found
        For split evolutions, returns a list where the last element might be a list of options
    """
    pokemon_name = pokemon_name.upper()
    
    # Check special chains first
    if pokemon_name in SPECIAL_CHAINS:
        return SPECIAL_CHAINS[pokemon_name]
    
    # Search through all chains for the pokemon
    for chain in SPECIAL_CHAINS.values():
        if pokemon_name in chain:
            start_idx = chain.index(pokemon_name)
            return chain[start_idx:]
        # Check in split evolution options
        for item in chain:
            if isinstance(item, list) and pokemon_name in item:
                return [pokemon_name]
    
    return None
