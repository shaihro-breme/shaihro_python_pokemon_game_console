import random
import combat_ui
from battle_ui import start_battle
from pokedex import get_all_pokemon
from save_system import save_game

def get_player_profile(pokemon_list):
    return {
        "player_name": input("Cual es tu nombre entrenador: "),
        "pokemon_inventory": [random.choice(pokemon_list) for _ in range(3)],
        "combats": 0,
        "pokeballs": 10,
        "health_potions": 5,
        "caught_ids": set(),
        "god_mode": False,
    }

def any_player_pokemon_lives(player_profile):
    return sum([p["current_health"] for p in player_profile["pokemon_inventory"]]) > 0

def choose_pokemon(player_profile):
    chosen = None
    while not chosen:
        print("Elige con que Pokemon luchar")
        for index, poke in enumerate(player_profile["pokemon_inventory"]):
            print(f"{index} - {get_pokemon_info(poke)}")
        try:
            return player_profile["pokemon_inventory"][int(input("Elige un Pokemon: "))]
        except (ValueError, IndexError):
            print("Opcion no valida")

def get_pokemon_info(pokemon):
    return f"{pokemon['name']} | lvl {pokemon['level']} | HP {pokemon['current_health']}/{pokemon['base_health']}"

def fight(player_profile, enemy_pokemon):
    start_battle(player_profile["pokemon_inventory"][0], enemy_pokemon, player_profile)

def main():
    print("\nCargando Pokedex")
    pokemon_list = get_all_pokemon()
    combat_ui.get_player_profile_func = lambda pokemons: get_player_profile(pokemons)
    player_profile = combat_ui.start_game()

    if player_profile.get("god_mode", False):
        print("\nMODO TEXTER AUTOMATICO ACTIVADO")

        while len(player_profile.get("caught_ids", [])) < 151:
            enemy_pokemon = random.choice(pokemon_list)

            if enemy_pokemon.get("dex_id") in player_profile["caught_ids"]:
                continue

            player_profile["caught_ids"].add(enemy_pokemon["dex_id"])
            player_profile["pokemon_inventory"].append(enemy_pokemon)
            player_profile["combats"] += 1

            print(f"Capturado {enemy_pokemon['name']}! "
                  f"({len(player_profile['caught_ids'])}/151) | Combates: {player_profile['combats']}")

        print("\nTEXTER ha completado la Pokédex 151/151 Pokémon capturados.")
        print(f"Total de combates simulados: {player_profile['combats']}")

    else:
        while any_player_pokemon_lives(player_profile):
            enemy_pokemon = random.choice(pokemon_list)
            fight(player_profile, enemy_pokemon)
            save_game(player_profile)
            player_profile["combats"] += 1

            print(f"\nCombates realizados: {player_profile['combats']}")

            if len(player_profile.get("caught_ids", [])) >= 151:
                print("\nFelicidades Has capturado los 151 Pokemon originales")
                break

    print(f"\nHas perdido en el combate numero {player_profile['combats']}")
    print("Gracias por jugar")

if __name__ == "__main__":
    main()