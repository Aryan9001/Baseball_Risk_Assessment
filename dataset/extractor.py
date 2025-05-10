# extractor.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
import cv2
import csv
import mediapipe as mp
from utils.angles import calculate_angle

# Define 6 joint triplets for angle calculation
POSE_ANGLE_JOINTS = {
    "left_elbow": [11, 13, 15],     # Shoulder, Elbow, Wrist
    "right_elbow": [12, 14, 16],
    "left_shoulder": [13, 11, 23],  # Elbow, Shoulder, Hip
    "right_shoulder": [14, 12, 24],
    "left_knee": [23, 25, 27],      # Hip, Knee, Ankle
    "right_knee": [24, 26, 28]
}

def extract_angles(landmarks):
    angles = []
    for joint_triplet in POSE_ANGLE_JOINTS.values():
        a = [landmarks[joint_triplet[0]].x, landmarks[joint_triplet[0]].y]
        b = [landmarks[joint_triplet[1]].x, landmarks[joint_triplet[1]].y]
        c = [landmarks[joint_triplet[2]].x, landmarks[joint_triplet[2]].y]
        angle = calculate_angle(a, b, c)
        angles.append(round(angle, 2))
    return angles


def generate_dataset(image_dir, output_csv):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)

    header = [
        "filename",
        "left_elbow", "right_elbow",
        "left_shoulder", "right_shoulder",
        "left_knee", "right_knee",
        "label"
    ]

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for label in os.listdir(image_dir):
            label_path = os.path.join(image_dir, label)
            if not os.path.isdir(label_path):
                continue

            for filename in os.listdir(label_path):
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue

                image_path = os.path.join(label_path, filename)
                image = cv2.imread(image_path)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    angles = extract_angles(landmarks)
                    writer.writerow([filename] + angles + [label])
                else:
                    print(f"⚠️ No pose detected in {filename}")

    print(f"✅ Dataset saved to: {output_csv}")


if __name__ == "__main__":
    generate_dataset("dataset", "injury_risk_dataset_new.csv")
