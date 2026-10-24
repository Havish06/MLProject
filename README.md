# Location-Aware Offline Plant Disease Detection

Small ML project (24BAI1524). Two stages:
1. **Sync (online):** GPS lat/lon → region → common regional diseases saved to `data/local_region.json`.
2. **Detect (offline):** image → preprocess → local Keras model → disease + confidence, filtered by the stored regional diseases.

## Structure
```
app/predictor.py     preprocessing + local prediction
app/sync.py          region lookup + local storage
app/main.py          Streamlit UI
prepare_dataset.py   sorts PlantVillage into dataset/<class>/
train.py             trains MobileNetV2, saves model + class order
```

## Dataset
Uses **PlantVillage** (Kaggle: "New Plant Diseases Dataset" / "PlantVillage"). Download and unzip it, then:
```
python prepare_dataset.py path/to/plantvillage 500
```
This builds `dataset/` with 4 classes (max 500 images each):

| Class | PlantVillage source folders |
|---|---|
| Bacterial Blight | *Bacterial spot* (tomato, pepper) - closest available match |
| Leaf Spot | Septoria / Cercospora leaf spot |
| Mosaic Viruses | Tomato mosaic virus |
| Powdery Mildew | Squash, cherry powdery mildew |

**Limitation:** Root Rot is not covered (PlantVillage is leaf-only). To add it, put root rot images in `dataset/Root Rot/` before training; `train.py` picks up the class count automatically.

## Run
```
pip install -r requirements.txt
python prepare_dataset.py PlantVillage 500
python train.py
streamlit run app/main.py
```
