# draw_overlay.py

import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_label_on_frame(frame, label, coords=(30, 30)):
    cv2.putText(frame, f"Risk: {label}", coords, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame

def draw_pose_and_angles(frame, landmarks, angles, joint_names):
    # Draw the full skeleton
    mp_drawing.draw_landmarks(
        frame,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
    )

    # Draw angles as text on joint positions (b-point of each triplet)
    for angle, joint_name in zip(angles, joint_names):
        joint_id = POSE_ANGLE_JOINTS[joint_name][1]  # middle point of the triplet
        joint = landmarks.landmark[joint_id]
        x, y = int(joint.x * frame.shape[1]), int(joint.y * frame.shape[0])
        cv2.putText(frame, f"{joint_name}: {int(angle)}°", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    return frame

# Re-declare joint map here to keep draw_overlay self-contained
POSE_ANGLE_JOINTS = {
    "left_elbow": [11, 13, 15],
    "right_elbow": [12, 14, 16],
    "left_shoulder": [13, 11, 23],
    "right_shoulder": [14, 12, 24],
    "left_knee": [23, 25, 27],
    "right_knee": [24, 26, 28]
}
