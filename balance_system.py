import random
from pokemon_types import type_effectiveness

def calculate_damage(attacker, defender, attack):
    base_damage = attack["damage"] * (attacker["level"] / 5)#antes estaba en 10

    multiplier = type_effectiveness(attack["type"], defender["type"])

    stab = 1.25 if attack["type"] in attacker["type"] else 1.0

    random_factor = random.uniform(0.9, 1.1)

    total_damage = base_damage * multiplier * stab * random_factor
    total_damage = int(max(1, total_damage))

    return total_damage

def calculate_experience(winner, loser):
    base_exp = 10
    level_diff = loser["level"] - winner["level"]

    exp_gain = base_exp + max(0, level_diff * 2)
    exp_gain *= random.uniform(0.8, 1.2)

    return exp_gain

def level_up(pokemon):
    while pokemon["current_exp"] >= 20:
        pokemon["current_exp"] -= 20
        pokemon["level"] += 1
        pokemon["base_health"] += 5
        pokemon["current_health"] = pokemon["base_health"]
        print(f"{pokemon['name']} ha subido al nivel {pokemon['level']}")

__all__ = ["calculate_damage", "calculate_experience", "level_up"]