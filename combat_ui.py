import os
import time
from save_system import load_game
from copy import deepcopy
from pokedex import get_all_pokemon

get_player_profile_func = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    clear_screen()
    print("=" * 43)
    print("         POKEMON")
    print("=" * 43)
    print()
    time.sleep(0.3)

def main_menu():
    print_title()
    print("[N] Nueva Partida")
    print("[P] Partidas Guardadas")
    print("[G] Modo TEXTER")
    print("[H] Ayuda Tutorial")
    print("[S] Salir")
    print("=" * 43)

    choice = input("Elige una opcion: ").strip().upper()
    return choice

def show_help():
    clear_screen()
    print("AYUDA DEL JUEGO POKEMON ADVENTURE")
    print()
    print("En este juego podras combatir capturar y entrenar Pokemon clasicos de la primera generacion")
    print()
    print("COMANDOS PRINCIPALES DURANTE EL COMBATE")
    print("[A] Atacar con uno de tus movimientos disponibles")
    print("[P] Usar una Pokeball para intentar capturar al enemigo")
    print("[V] Usar una pocion para curar 50 puntos de vida")
    print("[C] Cambiar de Pokemon")
    print()
    print("SISTEMA DE COMBATE")
    print("- Los ataques dependen del tipo y nivel del Pokemon")
    print("- Los tipos fuertes hacen 33 por ciento mas de dano")
    print("- Los tipos resistentes reciben 10 por ciento menos de dano")
    print("- La experiencia se gana al vencer enemigos")
    print()
    print("PARTIDAS GUARDADAS")
    print("- Se guardan automaticamente despues de cada combate")
    print("- Cada guardado es unico nombre_jugador_numero")
    print()
    print("OBJETIVO FINAL Capturar los 151 Pokemon originales")
    input("\nPresiona ENTER para volver al menu")

def god_mode():
    pokemon = {
        "name": "Texter",
        "level": 99,
        "dex_id": 999,
        "current_health": 999,
        "base_health": 999,
        "current_exp": 0,
        "type": ["Normal"],
        "attacks": [{
            "name": "Debug Blast",
            "type": "Normal",
            "damage": 999,
            "min_level": 1,
        }],
    }
    player_profile = {
        "player_name": "TEXTER_PLAYER",
        "pokemon_inventory": [deepcopy(pokemon)],
        "combats": 0,
        "pokeballs": 999999,
        "health_potions": 99,
        "caught_ids": {999},
        "god_mode": True,
    }

    print("Modo TEXTER activado Pokemon Texter agregado")
    input("Presiona ENTER para comenzar")
    return player_profile

def loading_screen():
    clear_screen()
    print("\nCargando", end="")
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print("\n")

def start_game():
    while True:
        choice = main_menu()
        if choice == "N":
            pokemon_list = get_all_pokemon()
            player_profile = get_player_profile_func(pokemon_list)
            player_profile["god_mode"] = False
            return player_profile

        elif choice == "P":
            player_profile = load_game()
            if player_profile:
                loading_screen()
                return player_profile
            input("Presiona ENTER para comenzar")

        elif choice == "G":
            return god_mode()

        elif choice == "H":
            show_help()

        elif choice == "S":
            confirm = input("Seguro que deseas salir S N ").strip().upper()
            if confirm == "S":
                print("Saliendo")
                time.sleep(1)
                exit()

        else:
            print("Opcion no valida intente nuevamente")
            time.sleep(1)