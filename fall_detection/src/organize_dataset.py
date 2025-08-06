import os
import shutil
import re

# Caminho onde estão todos os arquivos .mat
SOURCE_DIR = "../data/sameWindowData"
DEST_DIR = "../data/dataset"

def get_class_and_volunteer(filename):
    match = re.match(r'(\d)\.\d\.\d\.(\d{2})\.mat', filename)
    if match:
        cls = int(match.group(1))
        vol = int(match.group(2))
        return cls, vol
    else:
        return None, None

def organize_files():
    for fname in os.listdir(SOURCE_DIR):
        if not fname.endswith(".mat"):
            continue

        cls, vol = get_class_and_volunteer(fname)
        if cls is None:
            print(f"Filename not matched: {fname}")
            continue

        # Define split
        split = "train" if vol <= 18 else "test"
        label = "fall" if cls == 2 else "nonfall"

        dest_path = os.path.join(DEST_DIR, split, label)
        os.makedirs(dest_path, exist_ok=True)

        src_file = os.path.join(SOURCE_DIR, fname)
        dst_file = os.path.join(dest_path, fname)
        shutil.copy2(src_file, dst_file)

        print(f"Moved {fname} → {split}/{label}")

if __name__ == "__main__":
    organize_files()
