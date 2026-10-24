"""Sort a downloaded PlantVillage folder into dataset/<class>/ for train.py.
Usage: python prepare_dataset.py <path_to_plantvillage> [max_images_per_class]
Root Rot is not in PlantVillage, so this uses 4 classes
(Bacterial Blight is approximated by PlantVillage's 'Bacterial spot')."""
import random
import shutil
import sys
from pathlib import Path

# keyword in source folder name -> target class
RULES = [
    ("bacterial_spot", "Bacterial Blight"),
    ("leaf_spot", "Leaf Spot"),
    ("septoria", "Leaf Spot"),
    ("mosaic", "Mosaic Viruses"),
    ("powdery", "Powdery Mildew"),
]
IMG = {".jpg", ".jpeg", ".png"}

src = Path(sys.argv[1])
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 500
out = Path("dataset")

files = {}
for folder in src.rglob("*"):
    if not folder.is_dir():
        continue
    name = folder.name.lower()
    for key, cls in RULES:
        if key in name:
            files.setdefault(cls, []).extend(p for p in folder.iterdir() if p.suffix.lower() in IMG)
            break

if not files:
    sys.exit("No matching folders found - check the path.")

random.seed(0)
for cls, paths in sorted(files.items()):
    random.shuffle(paths)
    dest = out / cls
    dest.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(paths[:limit]):
        shutil.copy(p, dest / f"{i}{p.suffix.lower()}")
    print(f"{cls}: {min(len(paths), limit)} images (of {len(paths)})")
