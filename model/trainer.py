import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from config import CSV_DIR, MODEL_PATH, EPOCHS, BATCH_SIZE

def train_model():
    # Load dataset
    df = pd.read_csv(CSV_DIR)

    # Drop the filename column
    df = df.drop(columns=["filename"])

    # Features and labels
    X = df.drop(columns=["label"]).astype(np.float32).values
    y = LabelEncoder().fit_transform(df["label"])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define model
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X.shape[1],)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')  # 3 classes
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train
    model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.1)

    # Save model
    model.save(MODEL_PATH)
    print(f"✅ Model trained and saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
