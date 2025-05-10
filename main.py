# main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cv2
import numpy as np
import mediapipe as mp
from utils.draw_overlay import draw_label_on_frame, draw_pose_and_angles
from model.predictor import load_model, predict_pose_risk
from utils.angles import calculate_angle

# Define the joint triplets for angle calculation
POSE_ANGLE_JOINTS = {
    "left_elbow": [11, 13, 15],
    "right_elbow": [12, 14, 16],
    "left_shoulder": [13, 11, 23],
    "right_shoulder": [14, 12, 24],
    "left_knee": [23, 25, 27],
    "right_knee": [24, 26, 28]
}

def extract_angles(landmarks):
    angles = []
    for joint_triplet in POSE_ANGLE_JOINTS.values():
        a = [landmarks[joint_triplet[0]].x, landmarks[joint_triplet[0]].y]
        b = [landmarks[joint_triplet[1]].x, landmarks[joint_triplet[1]].y]
        c = [landmarks[joint_triplet[2]].x, landmarks[joint_triplet[2]].y]
        angle = calculate_angle(a, b, c)
        angles.append(angle)
    return angles

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    model = load_model()

    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=False) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks
                angles = extract_angles(landmarks.landmark)
                label = predict_pose_risk(model, angles)

                # Draw pose, angles and label
                frame = draw_pose_and_angles(frame, landmarks, angles, list(POSE_ANGLE_JOINTS.keys()))
                frame = draw_label_on_frame(frame, label)
            else:
                frame = draw_label_on_frame(frame, "No Pose")

            out.write(frame)

    cap.release()
    out.release()
    print(f"✅ Processed video saved to: {output_path}")

if __name__ == "__main__":
    input_video = "media/input_videos/max_scherzer.mp4"       # Change this to your target video
    output_video = "media/output_videos/max_scherzer_labeled_overlay.mp4"
    process_video(input_video, output_video)
