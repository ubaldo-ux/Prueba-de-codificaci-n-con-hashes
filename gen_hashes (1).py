# gen_hashes.py
# Genera SHA-256 de todos los archivos en una carpeta y guarda un registro en pickle.

import hashlib
import os
import pickle

CHUNK = 8192
HASHFILE = "hashes.pickle"
TARGET_DIR = "./check"  # carpeta que contiene los archivos a registrar

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def generar_registro(target_dir):
    registro = {}
    for root, _, files in os.walk(target_dir):
        for fname in sorted(files):
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, target_dir)
            registro[rel] = file_sha256(full)
            print("Hasheado:", rel)
    return registro

def guardar_pickle(registro, out_path):
    with open(out_path, "wb") as f:
        pickle.dump(registro, f)
    print("Registro guardado en", out_path)

def main():
    if not os.path.isdir(TARGET_DIR):
        print("Directorio no encontrado:", TARGET_DIR)
        return
    registro = generar_registro(TARGET_DIR)
    guardar_pickle(registro, HASHFILE)

if __name__ == "__main__":
    main()
