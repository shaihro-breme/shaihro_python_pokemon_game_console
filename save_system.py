import os
import pickle
from datetime import datetime

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")

def save_game(player_profile):
    create_save_folder()
    player_name = player_profile["player_name"]

    save_name = make_save_name(player_name)
    save_path = os.path.join(SAVE_DIR, save_name + ".pkl")

    player_profile["last_save"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    with open(save_path, "wb") as file:
        pickle.dump(player_profile, file)

    print(f"Partida guardada en {save_path}")

def load_game():
    saves = list_saves()

    if not saves:
        print("No Hay Partida Guardada")
        return None

    print("Partidas guardadas Disponibles")
    for i, s in enumerate(saves, start=1):
        print(f"{i}. {s['name']} (Ultima vez {s['modified']})")

    try:
        choice = int(input("Elige el numero de la partida que deseas cargar: "))
        selected = saves[choice - 1]
        with open(selected["path"], "rb") as file:
            profile = pickle.load(file)
        print(f"Partida {selected['name']} cargada con exito")
        return profile
    except (ValueError, IndexError):
        print("Opcion no valida")
        return None

def make_save_name(player_name):
    create_save_folder()
    base = player_name.lower().replace(" ", "_")
    existing = [f for f in os.listdir(SAVE_DIR) if f.startswith(base)]

    if not existing:
        return f"{base}_1"

    nums = [int(f.split("_")[-1].split(".")[0])
            for f in existing
            if f.split("_")[-1].split(".")[0].isdigit()
            ]
    next_num = max(nums) + 1 if nums else 1
    return f"{base}_{next_num}"

def list_saves():
    create_save_folder()
    saves = []

    for file in os.listdir(SAVE_DIR):
        if file.endswith(".pkl"):
            path = os.path.join(SAVE_DIR, file)
            modified = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
            saves.append({
                "name": file.replace(".pkl", ""),
                "path": path,
                "modified": modified
            })

    saves.sort(key=lambda s: os.path.getmtime(s["path"]), reverse=True)
    return saves

def create_save_folder():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)