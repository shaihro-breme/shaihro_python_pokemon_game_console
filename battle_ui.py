import random
import time
from balance_system import calculate_damage, calculate_experience, level_up
from pokemon_evolution import can_evolve, evolve
from save_system import save_game
from pokemon_types import type_effectiveness
from combat_ui import clear_screen
from pokedex import get_all_pokemon

def show_battle_status(player_pokemon, enemy_pokemon):
    clear_screen()
    print("\n" + "=" * 40)
    print(f"{player_pokemon['name']} (Lvl {player_pokemon['level']}) VS {enemy_pokemon['name']} (Lvl {enemy_pokemon['level']})")
    print(f"{player_pokemon['name']}: {player_pokemon['current_health']}/{player_pokemon['base_health']} HP")
    print(f"{enemy_pokemon['name']}: {enemy_pokemon['current_health']}/{enemy_pokemon['base_health']} HP")
    print("=" * 40)

def choose_attack(pokemon):
    valid_attacks = [atk for atk in pokemon["attacks"] if int(atk["min_level"]) <= pokemon["level"]]
    print("\nAtaques Disponibles")
    for i, atk in enumerate(valid_attacks, start=1):
        print(f"{i}. {atk['name']} (Tipo {atk['type']} Daño {atk['damage']})")

    choice = None
    while choice is None:
        try:
            choice = int(input("Elige un ataque: ")) - 1
            return valid_attacks[choice]
        except (ValueError, IndexError):
            print("Opcion no valida intenta nuevamente")

def player_turn(player_pokemon, enemy_pokemon, player_profile):
    show_battle_status(player_pokemon, enemy_pokemon)
    print("\n[A] Atacar  [P] Pokeball  [V] Curar  [C] Cambiar Pokemon")
    action = input("Elige una accion: ").upper()

    if action == "A":
        attack = choose_attack(player_pokemon)
        damage = calculate_damage(player_pokemon, enemy_pokemon, attack)
        enemy_pokemon["current_health"] = max(0, enemy_pokemon["current_health"] - damage)
        print(f"\n{player_pokemon['name']} usa {attack['name']} y causa {damage} de dano")
        multiplier = type_effectiveness(attack["type"], enemy_pokemon["type"])
        if multiplier == 0:
            print("No tuvo efecto")
        elif multiplier > 1:
            print("Es super eficaz")
        elif multiplier < 1:
            print("No es muy eficaz")
        return "attack"

    elif action == "P":
        if player_profile.get("god_mode", False):
            auto_capture_all(player_profile)
            return "capture_all"

        if player_profile["pokeballs"] <= 0:
            print("No tienes Pokeballs")
            return None
        player_profile["pokeballs"] -= 1
        succes = attempt_capture(enemy_pokemon, player_profile)
        if succes:
            print(f"Has capturado a {enemy_pokemon['name']}")
            player_profile["pokemon_inventory"].append(enemy_pokemon)
            player_profile["caught_ids"].add(enemy_pokemon.get("dex_id", random.randint(1, 151)))
            enemy_pokemon["current_health"] = 0
            return "capture"
        else:
            print("El Pokemon se escapo")
        return "pokeball"

    elif action == "V":
        if player_profile["health_potions"] <= 0:
            print("No te quedan pociones")
            return None
        player_profile["health_potions"] -= 1
        heal_amount = min(50, player_pokemon["base_health"] - player_pokemon["current_health"])
        player_pokemon["current_health"] += heal_amount
        print(f"{player_pokemon['name']} recupero {heal_amount} HP")
        return "heal"

    elif action == "C":
        print("Cambiando Pokemon")
        return "change"

def enemy_turn(enemy_pokemon, player_pokemon):
    attack = random.choice([atk for atk in enemy_pokemon["attacks"] if int(atk["min_level"]) <= enemy_pokemon["level"]])
    damage = calculate_damage(enemy_pokemon, player_pokemon, attack)
    player_pokemon["current_health"] = max(0, player_pokemon["current_health"] - damage)
    print(f"\n{enemy_pokemon['name']} usa {attack['name']} y causa {damage} de dano")

def attempt_capture(enemy_pokemon, player_profile):
    if player_profile.get("god_mode", False):
        print(f"TEXTER MODE {enemy_pokemon['name']} fue capturado automaticamente")
        player_profile["pokemon_inventory"].append(enemy_pokemon)
        player_profile["caught_ids"].add(enemy_pokemon.get("dex_id", -1))
        return True

    if player_profile["pokeballs"] <= 0:
        print("No tienes PokeBalls disponibles")
        return False

    player_profile["pokeballs"] -= 1
    hp_ratio = enemy_pokemon["current_health"] / enemy_pokemon["base_health"]

    if enemy_pokemon["current_health"] > 20 and not enemy_pokemon.get("stunned", False):
        chance = 0.01
    elif enemy_pokemon["current_health"] <= 20 and not enemy_pokemon.get("stunned", False):
        chance = 0.50#antes era 0.33
    elif enemy_pokemon.get("stunned", False):
        chance = 0.90#antes era 0.77
    else:
        chance = 0.01

    if random.random() < chance:
        print(f"Has capturado a {enemy_pokemon['name']}")
        player_profile["pokemon_inventory"].append(enemy_pokemon)
        player_profile["caught_ids"].add(enemy_pokemon.get("dex_id", -1))

        if player_profile["used_pokeballs"] > 1:
            recovered = player_profile["used_pokeballs"] - 1
            player_profile["pokeballs"] += recovered
            print(f"Recuperaste {recovered} pokeballs del combate")

        player_profile["used_pokeballs"] = 0
        return True
    else:
        print(f"{enemy_pokemon['name']} escapo")
        return False

def auto_capture_all(player_profile):
    all_pokemon = get_all_pokemon()
    print("Modo TEXTER automatico activado capturando todos los Pokemon")
    while len(player_profile.get("caught_ids", [])) < 151:
        candidate = random.choice(all_pokemon)
        dex = candidate.get("dex_id", None)
        if dex in player_profile["caught_ids"]:
            continue
        player_profile["pokemon_inventory"].append(candidate)
        player_profile["caught_ids"].add(dex)
        print(f"Capturado {candidate['name']} | Total {len(player_profile['caught_ids'])}/151")
        time.sleep(0.05)
    print("Todos los Pokemon han sido capturados por TEXTER")

def start_battle(player_pokemon, enemy_pokemon, player_profile):
    clear_screen()
    print(f"Un {enemy_pokemon['name']} salvaje aparecio")

    while player_pokemon["current_health"] > 0 and enemy_pokemon["current_health"] > 0:
        result = player_turn(player_pokemon, enemy_pokemon, player_profile)
        if result == "capture_all":
            return "texter_auto"
        if enemy_pokemon["current_health"] <= 0:
            print(f"\n{enemy_pokemon['name']} fue derrotado")
            exp = calculate_experience(player_pokemon, enemy_pokemon)
            player_pokemon["current_exp"] += exp
            print(f"{player_pokemon['name']} gana {round(exp, 2)} de experiencia")
            if player_pokemon["current_exp"] >= 20:
                level_up(player_pokemon)
                if can_evolve(player_pokemon):
                    evolve(player_pokemon)
            break

        if result == "capture":
            break

        time.sleep(1)
        enemy_turn(enemy_pokemon, player_pokemon)
        if player_pokemon["current_health"] <= 0:
            print(f"\n{player_pokemon['name']} se ha debilitado")
            return "defeat"

    caught = len(player_profile.get("caught_ids", []))
    total = 151
    print("\n" + "=" * 40)
    print(f" POKÉMON CAPTURADOS: {caught}/{total} ")
    print("=" * 40)
    print()
    print(f"[{'█' * (caught * 20 // total):<20}] {round(caught / total * 100, 1)}% completado")