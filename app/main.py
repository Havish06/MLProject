import streamlit as st
from PIL import Image
from predictor import load_model, predict
from sync import sync, load_local

st.title("🌿 Location-Aware Offline Plant Disease Detection")


@st.cache_resource
def get_model():
    return load_model()


# ---- Stage 1: regional sync (needs internet) ----
st.header("1. Sync regional data")
c1, c2 = st.columns(2)
lat = c1.number_input("Latitude", value=13.08)
lon = c2.number_input("Longitude", value=80.27)
if st.button("Sync (online)"):
    d = sync(lat, lon)
    st.success(f"Stored data for {d['region']}: {', '.join(d['diseases'])}")

local = load_local()
if local:
    st.info(f"Offline data: {local['region']} → {', '.join(local['diseases'])}")

# ---- Stage 2: offline detection ----
st.header("2. Detect disease (offline)")
file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"]) or st.camera_input("...or take a photo")
if file:
    img = Image.open(file)
    st.image(img, width=300)
    res = predict(img, get_model(), local["diseases"] if local else None)
    st.success(f"**{res['disease']}** ({res['confidence']:.1%} confidence)")
