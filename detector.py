import mediapipe as mp
import json
from utils import calculate_angle

with open("yoga_poses.json") as f:
    yoga_data = json.load(f)

mp_pose = mp.solutions.pose

class PoseDetector:
    def __init__(self, pose_type="Squats"):
        self.counter = 0
        self.stage = None
        self.pose_type = pose_type
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def detect_pose(self, image, landmarks):
        if self.pose_type == "Squats":
            hip, knee, ankle = [landmarks[i] for i in [mp_pose.PoseLandmark.LEFT_HIP.value,
                                                       mp_pose.PoseLandmark.LEFT_KNEE.value,
                                                       mp_pose.PoseLandmark.LEFT_ANKLE.value]]
            angle = calculate_angle(hip, knee, ankle)
            if angle > 160:
                self.stage = "up"
            if angle < 90 and self.stage == "up":
                self.stage = "down"
                self.counter += 1
            return f"Squat Count: {self.counter}"

        elif self.pose_type == "Push-Ups":
            shoulder, elbow, wrist = [landmarks[i] for i in [mp_pose.PoseLandmark.LEFT_SHOULDER.value,
                                                              mp_pose.PoseLandmark.LEFT_ELBOW.value,
                                                              mp_pose.PoseLandmark.LEFT_WRIST.value]]
            angle = calculate_angle(shoulder, elbow, wrist)
            if angle > 160:
                self.stage = "up"
            if angle < 90 and self.stage == "up":
                self.stage = "down"
                self.counter += 1
            return f"Push-Up Count: {self.counter}"

        elif self.pose_type in yoga_data:
            matched = 0
            for joint, (min_angle, max_angle) in yoga_data[self.pose_type].items():
                joint_enum = getattr(mp_pose.PoseLandmark, joint)
                i = joint_enum.value
                a, b, c = landmarks[i-1], landmarks[i], landmarks[i+1]
                angle = calculate_angle(a, b, c)
                if min_angle <= angle <= max_angle:
                    matched += 1
            return f"{self.pose_type}: {'✅ Correct' if matched == len(yoga_data[self.pose_type]) else '⚠️ Incorrect'}"
