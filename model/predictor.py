# predictor.py

import tensorflow as tf
import numpy as np
from dataset.label_mapper import int_to_label
from config import MODEL_PATH

def load_model():
# NEW (relative path)
    return tf.keras.models.load_model("model/injury_classifier_model.h5")

def predict_pose_risk(model, features):
    prediction = model.predict(np.array([features]))
    class_index = np.argmax(prediction)
    return int_to_label(class_index)
