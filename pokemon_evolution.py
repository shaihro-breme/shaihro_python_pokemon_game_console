from pprint import pprint

EVOLUTION_TABLE = {
    "Bulbasaur": {"to": "Ivysaur", "level": 16},
    "Ivysaur": {"to": "Venusaur", "level": 32},
    "Charmander": {"to": "Charmeleon", "level": 16},
    "Charmeleon": {"to": "Charizard", "level": 36},
    "Squirtle": {"to": "Wartortle", "level": 16},
    "Wartortle": {"to": "Blastoise", "level": 36},
    "Caterpie": {"to": "Metapod", "level": 7},
    "Metapod": {"to": "Butterfree", "level": 10},
    "Weedle": {"to": "Kakuna", "level": 7},
    "Kakuna": {"to": "Beedrill", "level": 10},
    "Pidgey": {"to": "Pidgeotto", "level": 18},
    "Pidgeotto": {"to": "Pidgeot", "level": 36},
    "Rattata": {"to": "Raticate", "level": 20},
    "Spearow": {"to": "Fearow", "level": 20},
    "Ekans": {"to": "Arbok", "level": 22},
    "Sandshrew": {"to": "Sandslash", "level": 22},
    "Nidoran♀": {"to": "Nidorina", "level": 16},
    "Nidorina": {"to": "Nidoqueen", "level": 36},
    "Nidoran♂": {"to": "Nidorino", "level": 16},
    "Nidorino": {"to": "Nidoking", "level": 36},
    "Clefairy": {"to": "Clefable", "level": 25},
    "Vulpix": {"to": "Ninetales", "level": 25},
    "Jigglypuff": {"to": "Wigglytuff", "level": 25},
    "Zubat": {"to": "Golbat", "level": 22},
    "Oddish": {"to": "Gloom", "level": 21},
    "Gloom": {"to": "Vileplume", "level": 36},
    "Paras": {"to": "Parasect", "level": 24},
    "Venonat": {"to": "Venomoth", "level": 31},
    "Diglett": {"to": "Dugtrio", "level": 26},
    "Meowth": {"to": "Persian", "level": 28},
    "Psyduck": {"to": "Golduck", "level": 33},
    "Mankey": {"to": "Primeape", "level": 28},
    "Poliwag": {"to": "Poliwhirl", "level": 25},
    "Poliwhirl": {"to": "Poliwrath", "level": 36},
    "Abra": {"to": "Kadabra", "level": 16},
    "Kadabra": {"to": "Alakazam", "level": 36},
    "Machop": {"to": "Machoke", "level": 28},
    "Machoke": {"to": "Machamp", "level": 36},
    "Bellsprout": {"to": "Weepinbell", "level": 21},
    "Weepinbell": {"to": "Victreebel", "level": 36},
    "Geodude": {"to": "Graveler", "level": 25},
    "Graveler": {"to": "Golem", "level": 36},
    "Gastly": {"to": "Haunter", "level": 25},
    "Haunter": {"to": "Gengar", "level": 36},
    "Magikarp": {"to": "Gyarados", "level": 20},
    "Eevee": {"to": "Vaporeon", "level": 20},
}

def can_evolve(pokemon):
    name = pokemon["name"]
    if name not in EVOLUTION_TABLE:
        return False

    evo_data = EVOLUTION_TABLE[name]
    return pokemon["level"] >= evo_data["level"]

def evolve(pokemon):
    name = pokemon["name"]
    if not can_evolve(pokemon):
        return pokemon

    new_form = EVOLUTION_TABLE[name]["to"]
    print(f"{name} HA EVOLUCIONADO A {new_form}")

    pokemon["name"] = new_form
    pokemon["base_health"] = int(pokemon["base_health"] * 1.25)
    pokemon["current_health"] = pokemon["base_health"]

    pokemon["level"] += 1

    return pokemon

__all__ = ["EVOLUTION_TABLE", "can_evolve", "evolve"]