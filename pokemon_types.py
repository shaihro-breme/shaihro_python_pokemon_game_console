TYPE_CHART = {
    "Normal": {
        "weaknesses": ["Fighting"],
        "resistances": [],
        "immunities": ["Ghost"],
    },
    "Fire": {
        "weaknesses": ["Water", "Ground", "Rock"],
        "resistances": ["Fire", "Grass", "Ice", "Bug"],
        "immunities": [],
    },
    "Water": {
        "weaknesses": ["Electric", "Grass"],
        "resistances": ["Fire", "Water", "Ice", "Steel"],
        "immunities": [],
    },
    "Electric": {
        "weaknesses": ["Ground"],
        "resistances": ["Electric", "Flying", "Steel"],
        "immunities": [],
    },
    "Grass": {
        "weaknesses": ["Fire", "Ice", "Poison", "Flying", "Bug"],
        "resistances": ["Water", "Electric", "Grass", "Ground"],
        "immunities": [],
    },
    "Ice": {
        "weaknesses": ["Fire", "Fighting", "Rock", "Steel"],
        "resistances": ["Ice"],
        "immunities": [],
    },
    "Fighting": {
        "weaknesses": ["Flying", "Psychic", "Fairy"],
        "resistances": ["Bug", "Rock", "Dark"],
        "immunities": [],
    },
    "Poison": {
        "weaknesses": ["Ground", "Psychic"],
        "resistances": ["Grass", "Fighting", "Poison", "Bug", "Fairy"],
        "immunities": [],
    },
    "Ground": {
        "weaknesses": ["Water", "Grass", "Ice"],
        "resistances": ["Poison", "Rock"],
        "immunities": ["Electric"],
    },
    "Flying": {
        "weaknesses": ["Electric", "Ice", "Rock"],
        "resistances": ["Grass", "Fighting", "Bug"],
        "immunities": ["Ground"],
    },
    "Psychic": {
        "weaknesses": ["Bug", "Ghost", "Dark"],
        "resistances": ["Fighting", "Psychic"],
        "immunities": [],
    },
    "Bug": {
        "weaknesses": ["Fire", "Flying", "Rock"],
        "resistances": ["Grass", "Fighting", "Ground"],
        "immunities": [],
    },
    "Rock": {
        "weaknesses": ["Water", "Grass", "Fighting", "Ground", "Steel"],
        "resistances": ["Normal", "Fire", "Poison", "Flying"],
        "immunities": [],
    },
    "Ghost": {
        "weaknesses": ["Ghost", "Dark"],
        "resistances": ["Poison", "Bug"],
        "immunities": ["Normal", "Fighting"],
    },
    "Dragon": {
        "weaknesses": ["Ice", "Fairy"],
        "resistances": ["Fire", "Water", "Electric", "Grass"],
        "immunities": [],
    },
}

def type_effectiveness(attack_type, defender_types):
    if attack_type not in TYPE_CHART:
        return 1.0

    multiplier = 1.0
    for defender_type in defender_types:
        if defender_type not in TYPE_CHART:
            continue

        data = TYPE_CHART[defender_type]

        if attack_type in data["weaknesses"]:
            multiplier *= 1.33

        if attack_type in data["resistances"]:
            multiplier *= 0.9

        if defender_type in data["immunities"]:
            multiplier *= 0.0

    return round(multiplier, 2)

__all__ = ["TYPE_CHART", "type_effectiveness"]