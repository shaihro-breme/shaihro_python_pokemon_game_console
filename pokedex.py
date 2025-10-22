import os
import pickle
from requests_html import HTMLSession

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POKEFILE_PATH = os.path.join(BASE_DIR, "pokefile.pkl")

pokemon_base = {
    "dex_id": None,
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": None,
    "current_exp": 0
}

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="

def get_pokemon(index):
    url = "{}{}".format(URL_BASE, index)
    session = HTMLSession()
    new_pokemon = pokemon_base.copy()
    pokemon_page = session.get(url)

    new_pokemon["dex_id"] = index
    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text
    new_pokemon["type"] = []
    for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        new_pokemon["type"].append(img.attrs["alt"])

    new_pokemon["attacks"] = []
    for attack_item in pokemon_page.html.find(".pkmain")[-1].find("tr.check3"):
        attack = {
            "name": attack_item.find("td", first=True).find("a", first=True).text,
            "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
            "min_level": attack_item.find("th", first=True).text,
            "damage": int(attack_item.find("td")[3].text.replace("--", "0")),
        }
        new_pokemon["attacks"].append(attack)

    return new_pokemon

def get_all_pokemon():
    print("Ruta actual del pokefile:{}".format(POKEFILE_PATH))
    try:
        print('Cargando el archivo pokefile desde la base de datos')
        with open(POKEFILE_PATH, "rb") as pokefile:
            all_pokemon = pickle.load(pokefile)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        print('El archivo pokefile no se ha encontrado Descargando pokefile desde internet')
        all_pokemon = []
        for index in range(151):
            all_pokemon.append(get_pokemon(index + 1))
            print("*", end="")
        with open(POKEFILE_PATH, "wb") as pokefile:
            pickle.dump(all_pokemon, pokefile)
        print("\nDescarga completada")
    for i, p in enumerate(all_pokemon, start=1):
        if "dex_id" not in p or p.get("dex_id") is None:
            p["dex_id"] = i

    return all_pokemon

if __name__ == '__main__':
    all_pokemon = get_all_pokemon()