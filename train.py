"""Train a small MobileNetV2 classifier on dataset/<class>/ folders (see prepare_dataset.py).
Keras orders classes alphabetically; the order is saved to model/classes.json for the app."""
import json
from pathlib import Path
import tensorflow as tf

ds = tf.keras.utils.image_dataset_from_directory(
    "dataset", validation_split=0.2, subset="both", seed=0, image_size=(224, 224), batch_size=32
)
train_ds, val_ds = ds
classes = train_ds.class_names
print("Classes:", classes)

base = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights="imagenet")
base.trainable = False
model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1 / 255.0),
    base,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(len(classes), activation="softmax"),
])
model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(train_ds, validation_data=val_ds, epochs=5)

Path("model").mkdir(exist_ok=True)
model.save("model/disease_model.h5")
Path("model/classes.json").write_text(json.dumps(classes))
