"""Stage 1: regional data sync (needs internet in a real deployment).
Here the region lookup uses a small bundled table to keep the project simple;
swap `fetch_regional_data` for a real API call to go fully online."""
import json
from pathlib import Path

LOCAL_FILE = Path(__file__).resolve().parent.parent / "data" / "local_region.json"

# (name, lat_min, lat_max, lon_min, lon_max, common diseases) - illustrative values
REGIONS = [
    ("South India", 8, 16, 74, 81, ["Leaf Spot", "Bacterial Blight", "Mosaic Viruses"]),
    ("North India", 24, 32, 74, 84, ["Powdery Mildew", "Leaf Spot"]),
    ("East India", 20, 27, 84, 92, ["Bacterial Blight", "Leaf Spot"]),
    ("West India", 16, 24, 68, 74, ["Powdery Mildew", "Mosaic Viruses"]),
]
DEFAULT = ("Generic", ["Bacterial Blight", "Leaf Spot", "Mosaic Viruses", "Powdery Mildew"])


def identify_region(lat, lon):
    for name, a, b, c, d, diseases in REGIONS:
        if a <= lat <= b and c <= lon <= d:
            return name, diseases
    return DEFAULT


def sync(lat, lon):
    """Download (here: look up) regional disease info and store it on the device."""
    region, diseases = identify_region(lat, lon)
    data = {"lat": lat, "lon": lon, "region": region, "diseases": diseases}
    LOCAL_FILE.parent.mkdir(exist_ok=True)
    LOCAL_FILE.write_text(json.dumps(data, indent=2))
    return data


def load_local():
    """Read stored regional data (works offline). Returns None if never synced."""
    return json.loads(LOCAL_FILE.read_text()) if LOCAL_FILE.exists() else None
