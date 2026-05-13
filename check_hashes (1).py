# check_hashes.py
# Lee hashes.pickle, recalcula hashes actuales y detecta cambios.
# Lista archivos: modificados, nuevos y eliminados. Opcionalmente actualiza el pickle.

import hashlib
import os
import pickle

CHUNK = 8192
HASHFILE = "hashes.pickle"
TARGET_DIR = "./check"

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def cargar_pickle(path):
    if not os.path.exists(path):
        print("No existe el registro:", path)
        return None
    with open(path, "rb") as f:
        return pickle.load(f)

def generar_actuales(target_dir):
    actuales = {}
    for root, _, files in os.walk(target_dir):
        for fname in sorted(files):
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, target_dir)
            actuales[rel] = file_sha256(full)
    return actuales

def comparar(registro_viejo, actuales):
    modificados = []
    nuevos = []
    eliminados = []

    viejo_keys = set(registro_viejo.keys()) if registro_viejo else set()
    ahora_keys = set(actuales.keys())

    for f in ahora_keys & viejo_keys:
        if registro_viejo[f] != actuales[f]:
            modificados.append(f)
    for f in ahora_keys - viejo_keys:
        nuevos.append(f)
    for f in viejo_keys - ahora_keys:
        eliminados.append(f)

    return modificados, nuevos, eliminados

def main():
    if not os.path.isdir(TARGET_DIR):
        print("Directorio no encontrado:", TARGET_DIR)
        return

    registro_viejo = cargar_pickle(HASHFILE)
    actuales = generar_actuales(TARGET_DIR)

    if registro_viejo is None:
        print("No hay registro previo. Use gen_hashes.py para crear hashes.pickle primero.")
        return

    modificados, nuevos, eliminados = comparar(registro_viejo, actuales)

    if not (modificados or nuevos or eliminados):
        print("No se detectaron cambios en los archivos.")
    else:
        if modificados:
            print("\nArchivos modificados:")
            for f in modificados:
                print(" -", f)
        if nuevos:
            print("\nArchivos nuevos:")
            for f in nuevos:
                print(" +", f)
        if eliminados:
            print("\nArchivos eliminados:")
            for f in eliminados:
                print(" x", f)

        # Preguntar si se desea actualizar el registro
        resp = input("\n¿Deseas actualizar hashes.pickle con el estado actual? (s/n): ").strip().lower()
        if resp == "s":
            with open(HASHFILE, "wb") as out:
                pickle.dump(actuales, out)
            print("Registro actualizado.")
        else:
            print("Registro no actualizado. Puedes revisar modificaciones y actualizar manualmente.")

if __name__ == "__main__":
    main()
