# predictor.py

import tensorflow as tf
import numpy as np
from dataset.label_mapper import int_to_label
from config import MODEL_PATH

def load_model():
    return tf.keras.models.load_model("C:/Users/ASUS/Desktop/Pose_estimation/Baseball_Player_Tracking/injury_classifier_model.h5")

def predict_pose_risk(model, features):
    prediction = model.predict(np.array([features]))
    class_index = np.argmax(prediction)
    return int_to_label(class_index)
